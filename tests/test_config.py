"""Tests for configuration management."""

import pytest
import os
from pathlib import Path
from github_trending.config import Config, GitHubConfig, StorageConfig


class TestConfig:
    """Test configuration management."""
    
    def test_default_config(self):
        """Test loading default configuration."""
        config = Config()
        
        assert config.github.api_base_url == "https://api.github.com"
        assert config.github.timeout == 30
        assert config.storage.data_dir == "./data"
        assert config.logging.level == "INFO"
    
    def test_github_config(self):
        """Test GitHub configuration."""
        github_config = GitHubConfig(
            api_token="test_token",
            timeout=60
        )
        
        assert github_config.api_token == "test_token"
        assert github_config.timeout == 60
        assert github_config.api_base_url == "https://api.github.com"
    
    def test_storage_config_paths(self):
        """Test storage configuration paths."""
        storage = StorageConfig(data_dir="./test_data")
        
        assert storage.raw_dir == Path("./test_data/raw")
        assert storage.merged_dir == Path("./test_data/merged")
        assert storage.reports_dir == Path("./test_data/reports")
    
    def test_ensure_directories(self, tmp_path):
        """Test directory creation."""
        config = Config()
        config.storage.data_dir = str(tmp_path / "data")
        config.logging.file = str(tmp_path / "logs/app.log")
        
        config.ensure_directories()
        
        assert (tmp_path / "data" / "raw").exists()
        assert (tmp_path / "data" / "merged").exists()
        assert (tmp_path / "data" / "reports").exists()
        assert (tmp_path / "logs").exists()
