"""Tests for data models."""

import pytest
from datetime import datetime
from github_trending.models import TrendingProject, TrendPeriod, ReportMetadata


class TestTrendingProject:
    """Test TrendingProject model."""
    
    def test_create_project(self):
        """Test creating a project instance."""
        project = TrendingProject(
            repository_name="owner/repo",
            url="https://github.com/owner/repo",
            stars_total=1000,
            stars_period=100,
            captured_at=datetime.utcnow(),
            trend_period=TrendPeriod.WEEKLY
        )
        
        assert project.repository_name == "owner/repo"
        assert project.stars_total == 1000
        assert project.stars_period == 100
    
    def test_validate_valid_project(self):
        """Test validation of valid project."""
        project = TrendingProject(
            repository_name="owner/repo",
            url="https://github.com/owner/repo",
            stars_total=1000,
            stars_period=100,
            captured_at=datetime.utcnow(),
            trend_period=TrendPeriod.WEEKLY
        )
        
        assert project.validate() is True
    
    def test_validate_invalid_repository_name(self):
        """Test validation fails for invalid repository name."""
        project = TrendingProject(
            repository_name="invalid_name",
            url="https://github.com/owner/repo",
            stars_total=1000,
            stars_period=100,
            captured_at=datetime.utcnow(),
            trend_period=TrendPeriod.WEEKLY
        )
        
        assert project.validate() is False
    
    def test_validate_negative_stars(self):
        """Test validation fails for negative stars."""
        project = TrendingProject(
            repository_name="owner/repo",
            url="https://github.com/owner/repo",
            stars_total=-10,
            stars_period=100,
            captured_at=datetime.utcnow(),
            trend_period=TrendPeriod.WEEKLY
        )
        
        assert project.validate() is False
    
    def test_to_dict(self):
        """Test converting project to dictionary."""
        now = datetime.utcnow()
        project = TrendingProject(
            repository_name="owner/repo",
            description="Test repo",
            language="Python",
            url="https://github.com/owner/repo",
            stars_total=1000,
            stars_period=100,
            captured_at=now,
            trend_period=TrendPeriod.WEEKLY,
            topics=["test", "python"]
        )
        
        data = project.to_dict()
        
        assert data['repository_name'] == "owner/repo"
        assert data['language'] == "Python"
        assert data['trend_period'] == "weekly"
        assert data['topics'] == "test,python"
    
    def test_from_dict(self):
        """Test creating project from dictionary."""
        data = {
            'repository_name': "owner/repo",
            'url': "https://github.com/owner/repo",
            'stars_total': 1000,
            'stars_period': 100,
            'captured_at': datetime.utcnow().isoformat(),
            'trend_period': 'weekly',
            'topics': 'test,python'
        }
        
        project = TrendingProject.from_dict(data)
        
        assert project.repository_name == "owner/repo"
        assert project.trend_period == TrendPeriod.WEEKLY
        assert len(project.topics) == 2


class TestReportMetadata:
    """Test ReportMetadata model."""
    
    def test_create_metadata(self):
        """Test creating report metadata."""
        now = datetime.utcnow()
        metadata = ReportMetadata(
            generated_at=now,
            period=TrendPeriod.WEEKLY,
            total_projects=25,
            data_source="test.csv"
        )
        
        assert metadata.total_projects == 25
        assert metadata.period == TrendPeriod.WEEKLY
    
    def test_to_dict(self):
        """Test converting metadata to dictionary."""
        now = datetime.utcnow()
        metadata = ReportMetadata(
            generated_at=now,
            period=TrendPeriod.WEEKLY,
            total_projects=25,
            data_source="test.csv"
        )
        
        data = metadata.to_dict()
        
        assert data['total_projects'] == 25
        assert data['period'] == 'weekly'
        assert 'generated_at' in data
