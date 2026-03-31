"""Tests for CSV handler."""

import pytest
from pathlib import Path
from datetime import datetime
from github_trending.storage import CSVHandler
from github_trending.models import TrendingProject, TrendPeriod
from github_trending.exceptions import ValidationError, FileIOError


class TestCSVHandler:
    """Test CSV file operations."""
    
    @pytest.fixture
    def sample_projects(self):
        """Create sample projects for testing."""
        now = datetime.utcnow()
        return [
            TrendingProject(
                repository_name="owner1/repo1",
                description="Test repo 1",
                language="Python",
                url="https://github.com/owner1/repo1",
                stars_total=1000,
                stars_period=100,
                forks=50,
                captured_at=now,
                trend_period=TrendPeriod.WEEKLY,
                topics=["test", "python"]
            ),
            TrendingProject(
                repository_name="owner2/repo2",
                description="Test repo 2",
                language="JavaScript",
                url="https://github.com/owner2/repo2",
                stars_total=2000,
                stars_period=200,
                forks=100,
                captured_at=now,
                trend_period=TrendPeriod.WEEKLY
            )
        ]
    
    def test_save_projects(self, tmp_path, sample_projects):
        """Test saving projects to CSV."""
        handler = CSVHandler()
        output_dir = tmp_path / "raw"
        
        csv_file = handler.save_projects(
            sample_projects,
            output_dir=output_dir
        )
        
        assert csv_file.exists()
        assert csv_file.suffix == '.csv'
    
    def test_load_projects(self, tmp_path, sample_projects):
        """Test loading projects from CSV."""
        handler = CSVHandler()
        output_dir = tmp_path / "raw"
        
        # Save first
        csv_file = handler.save_projects(
            sample_projects,
            output_dir=output_dir
        )
        
        # Load
        loaded_projects = handler.load_projects(csv_file)
        
        assert len(loaded_projects) == 2
        assert loaded_projects[0].repository_name == "owner1/repo1"
        assert loaded_projects[1].language == "JavaScript"
    
    def test_save_empty_projects(self):
        """Test saving empty project list raises error."""
        handler = CSVHandler()
        
        with pytest.raises(ValidationError):
            handler.save_projects([])
    
    def test_load_nonexistent_file(self):
        """Test loading non-existent file raises error."""
        handler = CSVHandler()
        
        with pytest.raises(FileIOError):
            handler.load_projects(Path("nonexistent.csv"))
    
    def test_generate_filename(self, sample_projects):
        """Test filename generation."""
        handler = CSVHandler()
        filename = handler._generate_filename(sample_projects[0])
        
        assert filename.startswith("trending_")
        assert filename.endswith("_weekly.csv")
    
    def test_roundtrip(self, tmp_path, sample_projects):
        """Test save and load roundtrip."""
        handler = CSVHandler()
        output_dir = tmp_path / "raw"
        
        # Save
        csv_file = handler.save_projects(
            sample_projects,
            output_dir=output_dir
        )
        
        # Load
        loaded_projects = handler.load_projects(csv_file)
        
        # Compare
        assert len(loaded_projects) == len(sample_projects)
        for original, loaded in zip(sample_projects, loaded_projects):
            assert original.repository_name == loaded.repository_name
            assert original.stars_total == loaded.stars_total
            assert original.language == loaded.language
