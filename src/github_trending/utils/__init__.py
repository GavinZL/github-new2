"""Logging configuration and utilities."""

import logging
import sys
from pathlib import Path
from typing import Optional
from .config import get_config


def setup_logging(log_file: Optional[str] = None, log_level: Optional[str] = None) -> logging.Logger:
    """Setup logging configuration.
    
    Args:
        log_file: Optional log file path, overrides config
        log_level: Optional log level, overrides config
        
    Returns:
        Root logger instance
    """
    config = get_config()
    
    # Use provided values or fall back to config
    file_path = log_file or config.logging.file
    level = log_level or config.logging.level
    log_format = config.logging.format
    
    # Ensure log directory exists
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger('github_trending')
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # File handler
    file_handler = logging.FileHandler(file_path, encoding='utf-8')
    file_handler.setLevel(getattr(logging, level.upper()))
    file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f'github_trending.{name}')
