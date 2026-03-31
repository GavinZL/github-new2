"""GitHub Trending page scraper."""

import re
import time
from datetime import datetime
from typing import List, Optional
from bs4 import BeautifulSoup
import requests

from ..models import TrendingProject, TrendPeriod
from ..exceptions import NetworkError, ParseError
from ..utils import get_logger


logger = get_logger('collectors.trending_scraper')


class TrendingScraper:
    """Scraper for GitHub Trending page.
    
    This class scrapes the GitHub Trending page to extract information
    about trending repositories.
    """
    
    BASE_URL = "https://github.com/trending"
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """Initialize the scraper.
        
        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_trending(
        self,
        period: TrendPeriod = TrendPeriod.WEEKLY,
        language: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[TrendingProject]:
        """Fetch trending repositories.
        
        Args:
            period: Trend period (daily/weekly/monthly)
            language: Filter by programming language (optional)
            limit: Maximum number of projects to fetch
            
        Returns:
            List of TrendingProject instances
            
        Raises:
            NetworkError: If request fails
            ParseError: If parsing fails
        """
        url = self._build_url(period, language)
        logger.info(f"Fetching trending from: {url}")
        
        html_content = self._fetch_page(url)
        projects = self._parse_trending_page(html_content, period)
        
        if limit:
            projects = projects[:limit]
        
        logger.info(f"Successfully fetched {len(projects)} trending projects")
        return projects
    
    def _build_url(self, period: TrendPeriod, language: Optional[str] = None) -> str:
        """Build GitHub Trending URL.
        
        Args:
            period: Trend period
            language: Programming language filter
            
        Returns:
            Complete URL string
        """
        url = self.BASE_URL
        
        if language:
            url += f"/{language.lower()}"
        
        params = []
        if period == TrendPeriod.DAILY:
            params.append("since=daily")
        elif period == TrendPeriod.WEEKLY:
            params.append("since=weekly")
        elif period == TrendPeriod.MONTHLY:
            params.append("since=monthly")
        
        if params:
            url += "?" + "&".join(params)
        
        return url
    
    def _fetch_page(self, url: str) -> str:
        """Fetch HTML content from URL with retry logic.
        
        Args:
            url: Target URL
            
        Returns:
            HTML content as string
            
        Raises:
            NetworkError: If all retry attempts fail
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                last_exception = e
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(
                    f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}. "
                    f"Retrying in {wait_time}s..."
                )
                if attempt < self.max_retries - 1:
                    time.sleep(wait_time)
        
        raise NetworkError(f"Failed to fetch {url} after {self.max_retries} attempts") from last_exception
    
    def _parse_trending_page(self, html: str, period: TrendPeriod) -> List[TrendingProject]:
        """Parse trending repositories from HTML.
        
        Args:
            html: HTML content
            period: Trend period
            
        Returns:
            List of TrendingProject instances
            
        Raises:
            ParseError: If parsing fails
        """
        try:
            soup = BeautifulSoup(html, 'lxml')
            projects = []
            captured_at = datetime.utcnow()
            
            # Find all repository articles
            articles = soup.find_all('article', class_='Box-row')
            
            if not articles:
                # Try alternative structure
                articles = soup.find_all('div', class_='Box-row')
            
            logger.debug(f"Found {len(articles)} repository articles")
            
            for article in articles:
                try:
                    project = self._parse_repository_article(article, period, captured_at)
                    if project and project.validate():
                        projects.append(project)
                    else:
                        logger.warning("Skipping invalid project data")
                except Exception as e:
                    logger.warning(f"Failed to parse repository article: {e}")
                    continue
            
            return projects
            
        except Exception as e:
            raise ParseError(f"Failed to parse trending page: {e}") from e
    
    def _parse_repository_article(
        self,
        article,
        period: TrendPeriod,
        captured_at: datetime
    ) -> Optional[TrendingProject]:
        """Parse a single repository article.
        
        Args:
            article: BeautifulSoup article element
            period: Trend period
            captured_at: Capture timestamp
            
        Returns:
            TrendingProject instance or None
        """
        # Extract repository name
        h2 = article.find('h2', class_='h3')
        if not h2:
            h2 = article.find('h1', class_='h3')
        
        if not h2:
            logger.debug("No h2/h1 tag found in article")
            return None
        
        repo_link = h2.find('a')
        if not repo_link:
            logger.debug("No link found in repository header")
            return None
        
        repo_name = repo_link.get('href', '').strip('/')
        if not repo_name:
            return None
        
        url = f"https://github.com/{repo_name}"
        
        # Extract description
        description_elem = article.find('p', class_='col-9')
        description = description_elem.get_text(strip=True) if description_elem else None
        
        # Extract language
        language = None
        lang_elem = article.find('span', {'itemprop': 'programmingLanguage'})
        if lang_elem:
            language = lang_elem.get_text(strip=True)
        
        # Extract stars in period
        stars_period = 0
        stars_span = article.find('span', class_='d-inline-block float-sm-right')
        if stars_span:
            stars_text = stars_span.get_text(strip=True)
            # Extract number from text like "1,234 stars this week"
            match = re.search(r'([\d,]+)\s+stars?', stars_text)
            if match:
                stars_period = int(match.group(1).replace(',', ''))
        
        # Extract total stars (from star button)
        stars_total = 0
        star_link = article.find('a', href=re.compile(r'/stargazers$'))
        if star_link:
            stars_text = star_link.get_text(strip=True)
            # Remove commas and convert to int
            stars_total = int(stars_text.replace(',', ''))
        
        return TrendingProject(
            repository_name=repo_name,
            description=description,
            language=language,
            stars_total=stars_total,
            stars_period=stars_period,
            url=url,
            captured_at=captured_at,
            trend_period=period
        )
    
    def close(self):
        """Close the session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
