from datetime import datetime
import os
from pathlib import Path
from typing import Optional
from src.domain.model import ConversionRequest, SourceFormat
from src.domain.ports import PDFConverterPort, FileSystemPort, ArchiverPort
from src.domain.exceptions import UnsupportedFormatError, ConversionError
from src.infrastructure.logger import logger

class ConversionService:
    def __init__(self, converter: PDFConverterPort, fs: FileSystemPort, archiver: Optional[ArchiverPort] = None):
        self.converter = converter
        self.fs = fs
        self.archiver = archiver

    def __get_format(self, path: str) -> SourceFormat:
        ext = Path(path).suffix.lower()
        if ext in ['.md', '.markdown']:
            return SourceFormat.MARKDOWN
        elif ext == '.txt':
            return SourceFormat.TEXT
        else:
            logger.error(f"Unsupported extension: {ext} for file {path}")
            raise UnsupportedFormatError(f"Unsupported file format: {ext}")

    def convert_file(self, input_path: str, output_path: str) -> str:
        """
        Orchestrates the conversion of a file to PDF.
        """
        logger.info(f"Starting conversion job: {input_path} -> {output_path}")
        
        # 1. Read Content
        content = self.fs.read_file(input_path)
        
        # 2. Determine Format
        source_format = self.__get_format(input_path)
        
        # 3. Create Request
        request = ConversionRequest(
            content=content,
            source_format=source_format,
            output_filename=os.path.basename(output_path),
            created_at=datetime.now()
        )
        
        # 4. Convert
        output_dir = os.path.dirname(output_path)
        if not output_dir:
            output_dir = "."
            
        result = self.converter.convert(request, output_dir)
        
        # 5. Archive (Project History)
        if self.archiver:
            self.archiver.archive(request, result)
        
        if not result.success:
            logger.error(f"Conversion failed: {result.error_message}")
            raise ConversionError(f"Conversion failed: {result.error_message}")
            
        logger.info(f"Conversion successful. Size: {result.size_bytes} bytes")
        return result.file_path
