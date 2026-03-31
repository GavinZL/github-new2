"""Collectors package initialization."""

from .trending_scraper import TrendingScraper
from .github_api import GitHubAPIClient

__all__ = ['TrendingScraper', 'GitHubAPIClient']
