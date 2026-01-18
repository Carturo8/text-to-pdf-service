import os
import sys
import glob
import logging
from pathlib import Path

# Add src to pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.adapters.driven.fs_adapter import LocalFileSystemAdapter
from src.adapters.driven.pdf_adapter import Xhtml2PdfAdapter
from src.adapters.driven.fs_archiver import FileSystemArchiver
from src.application.service import ConversionService
from src.infrastructure.logger import logger

def process_files():
    input_dir = Path("data/input")
    output_dir = Path("data/output")
    
    # Ensure dirs exist
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Init service
    fs_adapter = LocalFileSystemAdapter()
    pdf_adapter = Xhtml2PdfAdapter()
    archiver = FileSystemArchiver()
    service = ConversionService(pdf_adapter, fs_adapter, archiver)
    
    files = list(input_dir.glob("*.md")) + list(input_dir.glob("*.txt"))
    
    if not files:
        print(f"No files found in {input_dir}. Add .md or .txt files there.")
        return

    print(f"Found {len(files)} files. Processing...")
    
    for file_path in files:
        output_filename = f"{file_path.stem}.pdf"
        output_path = output_dir / output_filename
        
        try:
            print(f"Converting: {file_path.name}...")
            result = service.convert_file(str(file_path), str(output_path))
            print(f"  -> Generated: {result}")
        except Exception as e:
            print(f"  -> Error: {e}")

if __name__ == "__main__":
    process_files()
