"""Custom exceptions for GitHub Trending system."""


class GitHubTrendingError(Exception):
    """Base exception for GitHub Trending system."""
    pass


class ConfigurationError(GitHubTrendingError):
    """Configuration related errors."""
    pass


class DataCollectionError(GitHubTrendingError):
    """Data collection related errors."""
    pass


class NetworkError(DataCollectionError):
    """Network and API request errors."""
    pass


class RateLimitError(NetworkError):
    """GitHub API rate limit exceeded."""
    
    def __init__(self, reset_time: int, message: str = "API rate limit exceeded"):
        self.reset_time = reset_time
        super().__init__(f"{message}. Resets at: {reset_time}")


class ParseError(DataCollectionError):
    """HTML/Data parsing errors."""
    pass


class StorageError(GitHubTrendingError):
    """Data storage related errors."""
    pass


class FileIOError(StorageError):
    """File I/O operation errors."""
    pass


class ValidationError(GitHubTrendingError):
    """Data validation errors."""
    pass


class ReportGenerationError(GitHubTrendingError):
    """Report generation related errors."""
    pass


class TemplateError(ReportGenerationError):
    """Template loading and rendering errors."""
    pass
