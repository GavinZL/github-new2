"""GitHub API client for fetching repository details."""

import time
from datetime import datetime
from typing import Dict, Any, Optional, List
import requests

from ..models import TrendingProject
from ..exceptions import NetworkError, RateLimitError
from ..config import get_config
from ..utils import get_logger


logger = get_logger('collectors.github_api')


class GitHubAPIClient:
    """Client for GitHub REST API.
    
    This class provides methods to fetch detailed repository information
    using the GitHub REST API.
    """
    
    def __init__(self, api_token: Optional[str] = None, timeout: int = 30):
        """Initialize the API client.
        
        Args:
            api_token: GitHub Personal Access Token (optional)
            timeout: Request timeout in seconds
        """
        config = get_config()
        self.api_token = api_token or config.github.api_token
        self.base_url = config.github.api_base_url
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set headers
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Trending-Collector'
        }
        
        if self.api_token:
            headers['Authorization'] = f'token {self.api_token}'
            logger.info("Using authenticated API requests")
        else:
            logger.warning("No API token provided, rate limits will be restrictive")
        
        self.session.headers.update(headers)
    
    def enrich_project(self, project: TrendingProject) -> TrendingProject:
        """Enrich project with detailed information from GitHub API.
        
        Args:
            project: TrendingProject instance to enrich
            
        Returns:
            Enriched TrendingProject instance
            
        Raises:
            NetworkError: If API request fails
            RateLimitError: If rate limit is exceeded
        """
        try:
            repo_data = self.get_repository(project.repository_name)
            
            # Update project with API data
            project.stars_total = repo_data.get('stargazers_count', project.stars_total)
            project.forks = repo_data.get('forks_count', 0)
            project.open_issues = repo_data.get('open_issues_count', 0)
            
            # Parse dates
            created_at_str = repo_data.get('created_at')
            if created_at_str:
                project.created_at = datetime.strptime(created_at_str, '%Y-%m-%dT%H:%M:%SZ')
            
            updated_at_str = repo_data.get('updated_at')
            if updated_at_str:
                project.updated_at = datetime.strptime(updated_at_str, '%Y-%m-%dT%H:%M:%SZ')
            
            # Update language if not already set
            if not project.language and repo_data.get('language'):
                project.language = repo_data['language']
            
            # Update description if not already set
            if not project.description and repo_data.get('description'):
                project.description = repo_data['description']
            
            # Extract topics
            project.topics = repo_data.get('topics', [])
            
            # Extract license
            license_info = repo_data.get('license')
            if license_info:
                project.license = license_info.get('name') or license_info.get('spdx_id')
            
            logger.debug(f"Enriched project: {project.repository_name}")
            return project
            
        except RateLimitError:
            logger.warning(f"Rate limit hit, skipping enrichment for {project.repository_name}")
            raise
        except Exception as e:
            logger.warning(f"Failed to enrich {project.repository_name}: {e}")
            return project
    
    def get_repository(self, repo_name: str) -> Dict[str, Any]:
        """Get repository information.
        
        Args:
            repo_name: Repository name in format 'owner/repo'
            
        Returns:
            Repository data dictionary
            
        Raises:
            NetworkError: If request fails
            RateLimitError: If rate limit is exceeded
        """
        url = f"{self.base_url}/repos/{repo_name}"
        return self._make_request(url)
    
    def get_rate_limit(self) -> Dict[str, Any]:
        """Get current rate limit status.
        
        Returns:
            Rate limit information
        """
        url = f"{self.base_url}/rate_limit"
        try:
            return self._make_request(url)
        except Exception as e:
            logger.error(f"Failed to get rate limit: {e}")
            return {}
    
    def _make_request(self, url: str) -> Dict[str, Any]:
        """Make API request with error handling.
        
        Args:
            url: Target URL
            
        Returns:
            Response data as dictionary
            
        Raises:
            NetworkError: If request fails
            RateLimitError: If rate limit is exceeded
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            
            # Check rate limit
            if response.status_code == 403:
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                if reset_time:
                    raise RateLimitError(reset_time)
            
            response.raise_for_status()
            return response.json()
            
        except RateLimitError:
            raise
        except requests.RequestException as e:
            raise NetworkError(f"API request failed: {e}") from e
    
    def wait_for_rate_limit_reset(self, reset_time: int):
        """Wait for rate limit to reset.
        
        Args:
            reset_time: Unix timestamp when rate limit resets
        """
        current_time = int(time.time())
        wait_seconds = max(0, reset_time - current_time)
        
        if wait_seconds > 0:
            logger.info(f"Waiting {wait_seconds} seconds for rate limit reset...")
            time.sleep(wait_seconds + 1)  # Add 1 second buffer
    
    def enrich_projects_batch(
        self,
        projects: List[TrendingProject],
        delay: float = 0.5
    ) -> List[TrendingProject]:
        """Enrich multiple projects with API data.
        
        Args:
            projects: List of TrendingProject instances
            delay: Delay between requests in seconds
            
        Returns:
            List of enriched projects
        """
        enriched = []
        
        for i, project in enumerate(projects):
            try:
                enriched_project = self.enrich_project(project)
                enriched.append(enriched_project)
                
                # Add delay between requests to avoid hitting rate limits
                if i < len(projects) - 1:
                    time.sleep(delay)
                    
            except RateLimitError as e:
                logger.warning("Rate limit exceeded, waiting for reset...")
                self.wait_for_rate_limit_reset(e.reset_time)
                # Retry current project
                try:
                    enriched_project = self.enrich_project(project)
                    enriched.append(enriched_project)
                except Exception as retry_error:
                    logger.error(f"Failed to enrich after retry: {retry_error}")
                    enriched.append(project)
            except Exception as e:
                logger.error(f"Failed to enrich project {project.repository_name}: {e}")
                enriched.append(project)
        
        return enriched
    
    def close(self):
        """Close the session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
