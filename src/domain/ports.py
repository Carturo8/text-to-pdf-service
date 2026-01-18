from abc import ABC, abstractmethod
from src.domain.model import ConversionRequest, ConversionResult

class PDFConverterPort(ABC):
    """
    Driven Port: Interface for the actual PDF generation adapter.
    """
    @abstractmethod
    def convert(self, request: ConversionRequest, output_dir: str) -> ConversionResult:
        pass

class FileSystemPort(ABC):
    """
    Driven Port: Interface for file system operations (reading source).
    """
    @abstractmethod
    def read_file(self, path: str) -> str:
        """Reads the content of a file."""
        pass
    
    @abstractmethod
    def save_file(self, path: str, content: bytes) -> str:
        """Saves bytes to a file path."""
        pass
        
    @abstractmethod
    def list_files(self, directory: str, extensions: list[str]) -> list[str]:
        """Lists files in a directory matching extensions."""
        pass

class ArchiverPort(ABC):
    """
    Driven Port: Interface for archiving processing history.
    """
    @abstractmethod
    def archive(self, request: ConversionRequest, result: ConversionResult) -> None:
        """Archives the input and output for project history."""
        pass
