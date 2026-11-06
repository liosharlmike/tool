class LiosharlError(Exception):
    """Base exception for application-level failures."""


class TargetValidationError(LiosharlError, ValueError):
    """Raised when a supplied target input is invalid or unsupported."""


class AuthorizationError(LiosharlError):
    """Raised when authorization requirements are not met."""


class ToolNotFoundError(LiosharlError):
    """Raised when an external security tool is required but unavailable."""


class ConfigurationError(LiosharlError):
    """Raised when configuration values are invalid or absent."""


class DatabaseError(LiosharlError):
    """Raised when database operations fail."""


class ProcessExecutionError(LiosharlError):
    """Raised when a system command fails unexpectedly."""


class ReportGenerationError(LiosharlError):
    """Raised when a report cannot be generated."""
