"""Test configuration for pytest."""

import pytest
from pathlib import Path


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create temporary data directory structure."""
    data_dir = tmp_path / "data"
    (data_dir / "raw").mkdir(parents=True)
    (data_dir / "merged").mkdir(parents=True)
    (data_dir / "reports").mkdir(parents=True)
    return data_dir


@pytest.fixture
def sample_csv_content():
    """Sample CSV content for testing."""
    return """repository_name,description,language,stars_total,stars_period,forks,open_issues,created_at,updated_at,url,topics,license,captured_at,trend_period
owner/repo,Test repository,Python,1000,100,50,10,2024-01-01T00:00:00,2024-01-15T00:00:00,https://github.com/owner/repo,test,MIT,2024-01-15T10:00:00,weekly"""
