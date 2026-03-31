"""CSV file handler for storing trending data."""

import csv
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from collections import OrderedDict

from ..models import TrendingProject, TrendPeriod
from ..exceptions import FileIOError, ValidationError
from ..config import get_config
from ..utils import get_logger


logger = get_logger('storage.csv_handler')


class CSVHandler:
    """Handler for CSV file operations.
    
    This class manages reading and writing trending project data
    to CSV files with proper formatting and validation.
    """
    
    # CSV column headers in order
    HEADERS = [
        'repository_name',
        'description',
        'language',
        'stars_total',
        'stars_period',
        'forks',
        'open_issues',
        'created_at',
        'updated_at',
        'url',
        'topics',
        'license',
        'captured_at',
        'trend_period'
    ]
    
    def __init__(self, encoding: Optional[str] = None):
        """Initialize CSV handler.
        
        Args:
            encoding: File encoding (defaults to config value)
        """
        config = get_config()
        self.encoding = encoding or config.storage.encoding
        self.storage_config = config.storage
    
    def save_projects(
        self,
        projects: List[TrendingProject],
        filename: Optional[str] = None,
        output_dir: Optional[Path] = None
    ) -> Path:
        """Save projects to CSV file.
        
        Args:
            projects: List of TrendingProject instances
            filename: Optional filename (auto-generated if not provided)
            output_dir: Output directory (defaults to config raw_dir)
            
        Returns:
            Path to saved CSV file
            
        Raises:
            FileIOError: If file write fails
            ValidationError: If data validation fails
        """
        if not projects:
            raise ValidationError("No projects to save")
        
        # Validate all projects
        invalid_projects = [p for p in projects if not p.validate()]
        if invalid_projects:
            logger.warning(f"Found {len(invalid_projects)} invalid projects, filtering them out")
            projects = [p for p in projects if p.validate()]
        
        if not projects:
            raise ValidationError("All projects failed validation")
        
        # Determine output directory and filename
        output_dir = output_dir or self.storage_config.raw_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if not filename:
            filename = self._generate_filename(projects[0])
        
        file_path = output_dir / filename
        
        # Write to CSV
        try:
            with open(file_path, 'w', newline='', encoding=self.encoding) as f:
                writer = csv.DictWriter(f, fieldnames=self.HEADERS)
                writer.writeheader()
                
                for project in projects:
                    row_data = project.to_dict()
                    # Ensure all headers are present
                    row = {header: row_data.get(header, '') for header in self.HEADERS}
                    writer.writerow(row)
            
            logger.info(f"Saved {len(projects)} projects to {file_path}")
            
            # Update merged file
            self._update_merged_file(projects)
            
            return file_path
            
        except IOError as e:
            raise FileIOError(f"Failed to write CSV file: {e}") from e
    
    def load_projects(self, file_path: Path) -> List[TrendingProject]:
        """Load projects from CSV file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of TrendingProject instances
            
        Raises:
            FileIOError: If file read fails
        """
        if not file_path.exists():
            raise FileIOError(f"File not found: {file_path}")
        
        projects = []
        
        try:
            with open(file_path, 'r', encoding=self.encoding) as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    try:
                        # Convert string values to appropriate types
                        row_data = self._parse_csv_row(row)
                        project = TrendingProject.from_dict(row_data)
                        projects.append(project)
                    except Exception as e:
                        logger.warning(f"Failed to parse row: {e}")
                        continue
            
            logger.info(f"Loaded {len(projects)} projects from {file_path}")
            return projects
            
        except IOError as e:
            raise FileIOError(f"Failed to read CSV file: {e}") from e
    
    def _parse_csv_row(self, row: dict) -> dict:
        """Parse CSV row and convert types.
        
        Args:
            row: CSV row as dictionary
            
        Returns:
            Parsed row dictionary
        """
        parsed = {}
        
        for key, value in row.items():
            if not value or value == 'N/A':
                parsed[key] = None
                continue
            
            # Convert integers
            if key in ['stars_total', 'stars_period', 'forks', 'open_issues']:
                try:
                    parsed[key] = int(value)
                except ValueError:
                    parsed[key] = 0
            # Convert datetimes
            elif key in ['created_at', 'updated_at', 'captured_at']:
                try:
                    parsed[key] = datetime.fromisoformat(value)
                except ValueError:
                    parsed[key] = None
            # Convert trend period
            elif key == 'trend_period':
                try:
                    parsed[key] = TrendPeriod(value)
                except ValueError:
                    parsed[key] = TrendPeriod.WEEKLY
            # Convert topics (comma-separated string to list)
            elif key == 'topics':
                parsed[key] = [t.strip() for t in value.split(',') if t.strip()]
            else:
                parsed[key] = value
        
        return parsed
    
    def _generate_filename(self, project: TrendingProject) -> str:
        """Generate filename based on project data.
        
        Args:
            project: Sample project to extract metadata
            
        Returns:
            Generated filename
        """
        date_str = project.captured_at.strftime('%Y-%m-%d')
        period = project.trend_period.value
        return f"trending_{date_str}_{period}.csv"
    
    def _update_merged_file(self, new_projects: List[TrendingProject]):
        """Update merged historical data file.
        
        Args:
            new_projects: Newly collected projects
        """
        if not new_projects:
            return
        
        period = new_projects[0].trend_period.value
        merged_file = self.storage_config.merged_dir / f"trending_all_{period}.csv"
        
        # Load existing projects if file exists
        existing_projects = []
        if merged_file.exists():
            try:
                existing_projects = self.load_projects(merged_file)
            except Exception as e:
                logger.warning(f"Failed to load existing merged file: {e}")
        
        # Combine and deduplicate
        all_projects = existing_projects + new_projects
        
        # Remove duplicates based on repository_name and captured_at
        seen = set()
        unique_projects = []
        for project in all_projects:
            key = (project.repository_name, project.captured_at.isoformat())
            if key not in seen:
                seen.add(key)
                unique_projects.append(project)
        
        # Sort by captured_at (newest first)
        unique_projects.sort(key=lambda p: p.captured_at, reverse=True)
        
        # Save merged file
        try:
            self.storage_config.merged_dir.mkdir(parents=True, exist_ok=True)
            
            with open(merged_file, 'w', newline='', encoding=self.encoding) as f:
                writer = csv.DictWriter(f, fieldnames=self.HEADERS)
                writer.writeheader()
                
                for project in unique_projects:
                    row_data = project.to_dict()
                    row = {header: row_data.get(header, '') for header in self.HEADERS}
                    writer.writerow(row)
            
            logger.info(f"Updated merged file with {len(unique_projects)} total projects")
            
        except Exception as e:
            logger.error(f"Failed to update merged file: {e}")
    
    def get_latest_file(self, period: TrendPeriod) -> Optional[Path]:
        """Get the most recent CSV file for a given period.
        
        Args:
            period: Trend period
            
        Returns:
            Path to latest file or None
        """
        pattern = f"trending_*_{period.value}.csv"
        files = sorted(self.storage_config.raw_dir.glob(pattern), reverse=True)
        return files[0] if files else None
