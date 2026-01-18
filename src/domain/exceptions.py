class DomainError(Exception):
    """Base exception for domain errors."""
    pass

class UnsupportedFormatError(DomainError):
    """Raised when the input file format is not supported."""
    pass

class ConversionError(DomainError):
    """Raised when the PDF conversion fails."""
    pass

class FileAccessError(DomainError):
    """Raised when the file system cannot be accessed."""
    pass
