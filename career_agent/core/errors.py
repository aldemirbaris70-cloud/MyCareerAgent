"""Application-specific exceptions."""


class CareerAgentError(Exception):
    """Base exception for expected application errors."""


class DocumentReadError(CareerAgentError):
    """Raised when a document cannot be read or has an unsupported format."""


class InputValidationError(CareerAgentError):
    """Raised when required input is missing or empty."""