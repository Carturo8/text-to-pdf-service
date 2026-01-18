import os
from src.adapters.driven.pdf_adapter import Xhtml2PdfAdapter
from src.domain.model import ConversionRequest, SourceFormat

def test_xhtml2pdf_adapter_creates_pdf(tmp_path):
    adapter = Xhtml2PdfAdapter()
    
    # Use temporary directory for output
    output_dir = str(tmp_path)
    
    req = ConversionRequest(
        content="# Integration Test\nTesting PDF generation.",
        source_format=SourceFormat.MARKDOWN,
        output_filename="test_output.pdf"
    )
    
    result = adapter.convert(req, output_dir)
    
    assert result.success is True
    assert os.path.exists(result.file_path)
    assert result.size_bytes > 0
    assert result.file_path.endswith("test_output.pdf")
