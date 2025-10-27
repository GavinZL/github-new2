"""Configuration management for GitHub Trending system."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class GitHubConfig:
    """GitHub API configuration."""
    api_token: Optional[str] = None
    api_base_url: str = "https://api.github.com"
    timeout: int = 30
    max_retries: int = 3


@dataclass
class StorageConfig:
    """Storage configuration."""
    data_dir: str = "./data"
    encoding: str = "utf-8-sig"
    
    @property
    def raw_dir(self) -> Path:
        """Get raw data directory."""
        return Path(self.data_dir) / "raw"
    
    @property
    def merged_dir(self) -> Path:
        """Get merged data directory."""
        return Path(self.data_dir) / "merged"
    
    @property
    def reports_dir(self) -> Path:
        """Get reports directory."""
        return Path(self.data_dir) / "reports"


@dataclass
class ReportConfig:
    """Report generation configuration."""
    template_dir: str = "./templates"
    auto_generate: bool = True


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    file: str = "logs/app.log"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@dataclass
class Config:
    """Main configuration class."""
    github: GitHubConfig = field(default_factory=GitHubConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    report: ReportConfig = field(default_factory=ReportConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    @classmethod
    def load(cls, config_file: Optional[str] = None) -> 'Config':
        """Load configuration from multiple sources with priority.
        
        Priority order (highest to lowest):
        1. Environment variables
        2. User config file (~/.github-trending/config.yaml)
        3. Project config file (./config.yaml)
        4. Provided config file
        5. Default values
        
        Args:
            config_file: Optional path to config file
            
        Returns:
            Config instance
        """
        # Load environment variables from .env file
        load_dotenv()
        
        config_data = {}
        
        # Load from provided config file
        if config_file and os.path.exists(config_file):
            config_data = cls._load_yaml(config_file)
        
        # Load from project config file
        project_config = Path("./config.yaml")
        if project_config.exists():
            project_data = cls._load_yaml(str(project_config))
            config_data = cls._merge_dict(config_data, project_data)
        
        # Load from user config file
        user_config = Path.home() / ".github-trending" / "config.yaml"
        if user_config.exists():
            user_data = cls._load_yaml(str(user_config))
            config_data = cls._merge_dict(config_data, user_data)
        
        # Override with environment variables
        env_overrides = cls._load_from_env()
        config_data = cls._merge_dict(config_data, env_overrides)
        
        # Create config instance
        return cls._from_dict(config_data)
    
    @staticmethod
    def _load_yaml(file_path: str) -> Dict[str, Any]:
        """Load YAML configuration file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Failed to load config file {file_path}: {e}")
            return {}
    
    @staticmethod
    def _load_from_env() -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {}
        
        # GitHub config
        if os.getenv('GITHUB_TOKEN') or os.getenv('GITHUB_API_TOKEN'):
            config.setdefault('github', {})
            config['github']['api_token'] = os.getenv('GITHUB_TOKEN') or os.getenv('GITHUB_API_TOKEN')
        
        if os.getenv('GITHUB_API_BASE_URL'):
            config.setdefault('github', {})
            config['github']['api_base_url'] = os.getenv('GITHUB_API_BASE_URL')
        
        if os.getenv('GITHUB_API_TIMEOUT'):
            config.setdefault('github', {})
            config['github']['timeout'] = int(os.getenv('GITHUB_API_TIMEOUT'))
        
        # Storage config
        if os.getenv('DATA_DIR'):
            config.setdefault('storage', {})
            config['storage']['data_dir'] = os.getenv('DATA_DIR')
        
        # Logging config
        if os.getenv('LOG_LEVEL'):
            config.setdefault('logging', {})
            config['logging']['level'] = os.getenv('LOG_LEVEL')
        
        return config
    
    @staticmethod
    def _merge_dict(base: Dict, override: Dict) -> Dict:
        """Recursively merge two dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = Config._merge_dict(result[key], value)
            else:
                result[key] = value
        return result
    
    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """Create Config instance from dictionary."""
        github_data = data.get('github', {})
        storage_data = data.get('storage', {})
        report_data = data.get('report', {})
        logging_data = data.get('logging', {})
        
        return cls(
            github=GitHubConfig(**github_data),
            storage=StorageConfig(**storage_data),
            report=ReportConfig(**report_data),
            logging=LoggingConfig(**logging_data)
        )
    
    def ensure_directories(self):
        """Ensure all required directories exist."""
        directories = [
            self.storage.raw_dir,
            self.storage.merged_dir,
            self.storage.reports_dir,
            Path(self.logging.file).parent,
            Path(self.report.template_dir)
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# Global config instance
_config: Optional[Config] = None


def get_config(config_file: Optional[str] = None, reload: bool = False) -> Config:
    """Get global configuration instance.
    
    Args:
        config_file: Optional path to config file
        reload: Force reload configuration
        
    Returns:
        Config instance
    """
    global _config
    if _config is None or reload:
        _config = Config.load(config_file)
        _config.ensure_directories()
    return _config
