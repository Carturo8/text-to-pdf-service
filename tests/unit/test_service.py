import pytest
from unittest.mock import Mock, MagicMock
from src.application.service import ConversionService
from src.domain.model import SourceFormat, ConversionResult
from src.domain.ports import PDFConverterPort, FileSystemPort

@pytest.fixture
def mock_fs():
    return Mock(spec=FileSystemPort)

@pytest.fixture
def mock_converter():
    return Mock(spec=PDFConverterPort)

def test_convert_file_markdown(mock_fs, mock_converter):
    # Setup
    service = ConversionService(mock_converter, mock_fs)
    mock_fs.read_file.return_value = "# Hello"
    
    expected_result = ConversionResult(
        file_path="/abs/out.pdf",
        size_bytes=100,
        success=True
    )
    mock_converter.convert.return_value = expected_result

    # Execute
    path = service.convert_file("input.md", "out.pdf")

    # Verify
    assert path == "/abs/out.pdf"
    mock_fs.read_file.assert_called_with("input.md")
    mock_converter.convert.assert_called_once()
    
    # Check request passed to converter has correct format
    call_args = mock_converter.convert.call_args
    request = call_args[0][0] # first arg
    assert request.source_format == SourceFormat.MARKDOWN
    assert request.content == "# Hello"

from src.domain.exceptions import UnsupportedFormatError
from src.infrastructure.logger import logger

def test_convert_file_unsupported_format(mock_fs, mock_converter):
    service = ConversionService(mock_converter, mock_fs)
    
    with pytest.raises(UnsupportedFormatError, match="Unsupported file format"):
        service.convert_file("input.jpg", "out.pdf")
