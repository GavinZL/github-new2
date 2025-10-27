"""Data models for GitHub Trending projects."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class TrendPeriod(Enum):
    """Trend period enumeration."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class TrendingProject:
    """Model for a GitHub trending project.
    
    Attributes:
        repository_name: Repository full name (owner/repo)
        description: Project description
        language: Primary programming language
        stars_total: Total star count
        stars_period: Stars gained in the period
        forks: Fork count
        open_issues: Open issue count
        created_at: Repository creation time
        updated_at: Last update time
        url: Repository URL
        topics: Project tags/topics
        license: License type
        captured_at: Data capture timestamp
        trend_period: Trend period (daily/weekly/monthly)
    """
    
    repository_name: str
    url: str
    stars_total: int
    stars_period: int
    captured_at: datetime
    trend_period: TrendPeriod
    
    description: Optional[str] = None
    language: Optional[str] = None
    forks: int = 0
    open_issues: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    topics: List[str] = field(default_factory=list)
    license: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with proper serialization."""
        data = asdict(self)
        # Convert datetime objects to ISO format strings
        data['captured_at'] = self.captured_at.isoformat() if self.captured_at else None
        data['created_at'] = self.created_at.isoformat() if self.created_at else None
        data['updated_at'] = self.updated_at.isoformat() if self.updated_at else None
        # Convert enum to string
        data['trend_period'] = self.trend_period.value
        # Convert list to comma-separated string for CSV compatibility
        data['topics'] = ','.join(self.topics) if self.topics else ''
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TrendingProject':
        """Create instance from dictionary."""
        # Parse datetime strings
        if isinstance(data.get('captured_at'), str):
            data['captured_at'] = datetime.fromisoformat(data['captured_at'])
        if isinstance(data.get('created_at'), str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if isinstance(data.get('updated_at'), str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        
        # Parse enum
        if isinstance(data.get('trend_period'), str):
            data['trend_period'] = TrendPeriod(data['trend_period'])
        
        # Parse topics
        if isinstance(data.get('topics'), str):
            data['topics'] = [t.strip() for t in data['topics'].split(',') if t.strip()]
        
        return cls(**data)
    
    def validate(self) -> bool:
        """Validate required fields."""
        if not self.repository_name or '/' not in self.repository_name:
            return False
        if not self.url:
            return False
        if self.stars_total < 0 or self.stars_period < 0:
            return False
        if not self.captured_at:
            return False
        return True


@dataclass
class ReportMetadata:
    """Metadata for generated reports.
    
    Attributes:
        generated_at: Report generation timestamp
        period: Trend period
        total_projects: Total number of projects
        data_source: Source CSV file path
        date_range_start: Start date of data
        date_range_end: End date of data
    """
    
    generated_at: datetime
    period: TrendPeriod
    total_projects: int
    data_source: str
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'generated_at': self.generated_at.isoformat(),
            'period': self.period.value,
            'total_projects': self.total_projects,
            'data_source': self.data_source,
            'date_range_start': self.date_range_start.isoformat() if self.date_range_start else None,
            'date_range_end': self.date_range_end.isoformat() if self.date_range_end else None,
        }
