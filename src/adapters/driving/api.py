from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import shutil
import os
import tempfile
import zipfile
import time
import uuid
from pathlib import Path

from src.adapters.driven.fs_adapter import LocalFileSystemAdapter
from src.adapters.driven.pdf_adapter import Xhtml2PdfAdapter
from src.adapters.driven.fs_archiver import FileSystemArchiver
from src.application.service import ConversionService
from src.domain.exceptions import UnsupportedFormatError, ConversionError
from src.infrastructure.logger import logger

app = FastAPI(
    title="Text to PDF Service",
    description="""
![Architecture](https://img.shields.io/badge/Hexagonal-Architecture-blue?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11+-yellow?style=for-the-badge&logo=python)

### Professional Document Conversion Service (V1)

This production-ready service converts Markdown and Text files into high-quality PDF documents using Hexagonal Architecture principles. 
Finalized with **Gemini 3 Flash**.

**Core Capabilities:**
- ⚡ **High Performance**: Fast conversion with request tracing (`X-Request-ID`) and process time reporting (`X-Process-Time`).
- 🛠️ **Robust Architecture**: Port-based design for extreme maintainability and scalability.
- 📦 **Multi-file Processing**: Upload single files, multiple files (packaged as ZIP), or trigger local batch processing.
- 🛡️ **Observability**: Real-time request tracking and detailed system logs.

---
*Developer:* **Carlos Arturo Rojas Bolaños**
""",
    version="1.0.0",
    contact={
        "name": "Carlos Arturo Rojas Bolaños",
        "url": "https://github.com/yourusername/text-to-pdf-service",
    },
    openapi_tags=[
        {"name": "Conversion", "description": "Core PDF generation operations"},
        {"name": "Status", "description": "Service health and monitoring: /health for uptime, / for basic info."},
        {"name": "Tools", "description": "Batch processing and dev utilities"},
    ]
)

# =============================================================================
# Middlewares (Pro Security & Tracing)
# =============================================================================

@app.middleware("http")
async def add_process_time_and_trace_id(request: Request, call_next):
    """
    Middleware to add X-Process-Time and X-Request-ID headers.
    Enables better observability and tracing.
    """
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    # Store request_id in state for access in endpoints if needed
    request.state.request_id = request_id
    
    # Log request start
    logger.info(f"[{request_id}] {request.method} {request.url.path} - Started")
    
    try:
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(round(process_time, 4))
        response.headers["X-Request-ID"] = request_id
        
        # Log request completion
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} - "
            f"Status: {response.status_code} - Time: {round(process_time, 4)}s"
        )
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"[{request_id}] {request.method} {request.url.path} - Failed: {str(e)}")
        raise e


# Basic CORS configuration (Safe for local and container use)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Health & Status Endpoints
# =============================================================================

@app.get("/health", summary="Health Check", tags=["Status"])
async def health_check():
    """
    Service health check endpoint for monitoring and load balancers.
    
    Returns current service status and version information.
    No authentication required.
    """
    return {
        "status": "healthy",
        "service": "text-to-pdf-service",
        "version": "1.0.0"
    }


@app.get("/", summary="Root", tags=["Status"])
async def root():
    """Welcome endpoint with service information."""
    return {
        "service": "Text to PDF Converter",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs",
        "health": "/health"
    }


def get_service() -> ConversionService:
    fs_adapter = LocalFileSystemAdapter()
    pdf_adapter = Xhtml2PdfAdapter()
    # Enable Archiver
    archiver = FileSystemArchiver()
    return ConversionService(pdf_adapter, fs_adapter, archiver)

def cleanup_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

@app.post("/convert/", summary="Convert File to PDF", tags=["Conversion"])
async def convert_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Upload a single text or markdown file and receive a professionally formatted PDF.
    
    **Supported formats**: `.md`, `.markdown`, `.txt`
    
    **Process**:
    1. File is validated and temporarily stored
    2. Content is converted to styled PDF
    3. PDF is returned and temporary files are cleaned up
    
    **Limits**: 
    - Single file per request
    - Max file size: 10MB
    
    **For bulk conversion**: Use `/bulk-convert` endpoint instead.
    """
    filename = file.filename
    ext = Path(filename).suffix.lower()
    
    # Validation
    if ext not in ['.md', '.markdown', '.txt']:
        logger.warning(f"Invalid file type attempted: {ext}")
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type '{ext}'. Only .md, .markdown, and .txt are supported."
        )
    
    # File sizes & validation
    MAX_SIZE = 10 * 1024 * 1024
    file_content = await file.read()
    
    if not file_content:
        logger.warning(f"Empty file uploaded: {filename}")
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )
        
    if len(file_content) > MAX_SIZE:
        logger.warning(f"File too large: {len(file_content)} bytes")
        raise HTTPException(
            status_code=413,
            detail="File size exceeds 10MB limit"
        )
    
    logger.info(f"Converting file: {filename} ({len(file_content)} bytes)")
    
    # Create temp files with unique names
    fd, input_path = tempfile.mkstemp(suffix=ext)
    os.close(fd)
    
    output_filename = f"{Path(filename).stem}.pdf"
    output_path = input_path + ".pdf"
    
    try:
        # Save uploaded content
        with open(input_path, "wb") as buffer:
            buffer.write(file_content)
            
        # Convert using service
        service = get_service()
        result_path = service.convert_file(input_path, output_path)
            
        # Schedule cleanup
        background_tasks.add_task(cleanup_file, input_path)
        background_tasks.add_task(cleanup_file, output_path)

        logger.info(f"Conversion successful: {output_filename}")
        
        return FileResponse(
            result_path, 
            media_type='application/pdf', 
            filename=output_filename
        )
    except UnsupportedFormatError as e:
        cleanup_file(input_path)
        cleanup_file(output_path)
        logger.error(f"Format error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except ConversionError as e:
        cleanup_file(input_path)
        cleanup_file(output_path)
        logger.error(f"Conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")
    except Exception:
        cleanup_file(input_path)
        cleanup_file(output_path)
        logger.exception("Unexpected error during conversion")
        raise HTTPException(status_code=500, detail="Internal server error during conversion")

@app.post("/bulk-convert", summary="Bulk File Conversion", tags=["Tools"])
async def bulk_convert():
    """
    Convert multiple files from local directory in a single operation.
    
    Scans `data/input` directory for `.md` and `.txt` files,
    converts them to PDF, and saves results to `data/output`.
    
    This endpoint is designed for batch processing workflows where
    multiple documents need to be converted efficiently.
    
    Returns a detailed summary of processing results including
    success/failure status for each file.
    """
    try:
        logger.info("Bulk conversion initiated via API")
        
        input_dir = Path("data/input")
        output_dir = Path("data/output")
        
        # Ensure directories exist
        input_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create adapters
        fs_adapter = LocalFileSystemAdapter()
        pdf_adapter = Xhtml2PdfAdapter()
        archiver = FileSystemArchiver()
        service = ConversionService(pdf_adapter, fs_adapter, archiver)
        
        # Discover files
        files = fs_adapter.list_files(str(input_dir), [".md", ".txt"])
        
        if not files:
            logger.warning(f"No files found in {input_dir}")
            return {
                "message": "No files found to process", 
                "processed": 0,
                "results": []
            }
        
        logger.info(f"Found {len(files)} file(s) to process")
        
        results = []
        success_count = 0
        
        for input_path in files:
            p_in = Path(input_path)
            output_filename = f"{p_in.stem}.pdf"
            output_path = output_dir / output_filename
            
            try:
                service.convert_file(str(input_path), str(output_path))
                results.append({
                    "file": p_in.name,
                    "status": "success",
                    "error": None
                })
                success_count += 1
            except Exception as conv_error:
                logger.error(f"Failed to convert {p_in.name}: {str(conv_error)}")
                results.append({
                    "file": p_in.name,
                    "status": "error",
                    "error": str(conv_error)
                })
        
        logger.info(f"Bulk conversion completed: {success_count}/{len(files)} successful")
        
        return {
            "message": "Bulk conversion completed",
            "processed": len(files),
            "successful": success_count,
            "failed": len(files) - success_count,
            "results": results
        }
        
    except Exception as e:
        logger.exception("Bulk conversion failed with unexpected error")
        raise HTTPException(
            status_code=500, 
            detail=f"Bulk conversion failed: {str(e)}"
        )


@app.post("/convert/multiple", summary="Convert Multiple Files", tags=["Conversion"])
async def convert_multiple_files(
    background_tasks: BackgroundTasks, 
    files: List[UploadFile] = File(...)
):
    """
    Upload multiple text or markdown files and receive a ZIP containing all PDFs.
    
    **Supported formats**: `.md`, `.markdown`, `.txt`
    
    **Process**:
    1. Each file is validated (type and size)
    2. All valid files are converted to PDF
    3. PDFs are packaged into a ZIP file
    4. ZIP is returned and temporary files are cleaned up
    
    **Limits**:
    - Max 20 files per request
    - Max 10MB per file
    - Total max 50MB per request
    
    **Response**: `application/zip` containing all generated PDFs
    """
    MAX_FILES = 20
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_TOTAL_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = ['.md', '.markdown', '.txt']
    
    # Validate file count
    if len(files) > MAX_FILES:
        raise HTTPException(
            status_code=400,
            detail=f"Too many files. Maximum {MAX_FILES} files allowed."
        )
    
    if len(files) == 0:
        raise HTTPException(
            status_code=400,
            detail="No files provided."
        )
    
    logger.info(f"Multi-file conversion initiated: {len(files)} files")
    
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "converted_pdfs.zip")
    
    try:
        service = get_service()
        results = []
        total_size = 0
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for upload_file in files:
                filename = upload_file.filename
                ext = Path(filename).suffix.lower()
                
                # Validate extension
                if ext not in ALLOWED_EXTENSIONS:
                    results.append({
                        "file": filename,
                        "status": "skipped",
                        "error": f"Unsupported format: {ext}"
                    })
                    continue
                
                # Read content
                content = await upload_file.read()
                file_size = len(content)
                
                if file_size == 0:
                    results.append({
                        "file": filename,
                        "status": "skipped",
                        "error": "File is empty"
                    })
                    continue
                
                total_size += file_size
                
                # Validate sizes
                if file_size > MAX_FILE_SIZE:
                    results.append({
                        "file": filename,
                        "status": "skipped",
                        "error": "File exceeds 10MB limit"
                    })
                    continue
                
                if total_size > MAX_TOTAL_SIZE:
                    results.append({
                        "file": filename,
                        "status": "skipped",
                        "error": "Total request size exceeds 50MB limit"
                    })
                    continue
                
                # Create temp input file
                input_path = os.path.join(temp_dir, filename)
                output_filename = f"{Path(filename).stem}.pdf"
                output_path = os.path.join(temp_dir, output_filename)
                
                try:
                    with open(input_path, 'wb') as f:
                        f.write(content)
                    
                    service.convert_file(input_path, output_path)
                    
                    # Add to ZIP
                    zf.write(output_path, output_filename)
                    
                    results.append({
                        "file": filename,
                        "status": "success",
                        "output": output_filename
                    })
                    
                except Exception as conv_err:
                    logger.error(f"Failed to convert {filename}: {str(conv_err)}")
                    results.append({
                        "file": filename,
                        "status": "error",
                        "error": str(conv_err)
                    })
        
        success_count = sum(1 for r in results if r["status"] == "success")
        logger.info(f"Multi-file conversion completed: {success_count}/{len(files)} successful")
        
        # Schedule cleanup
        background_tasks.add_task(shutil.rmtree, temp_dir, ignore_errors=True)
        
        return FileResponse(
            zip_path,
            media_type='application/zip',
            filename='converted_pdfs.zip',
            headers={"X-Conversion-Results": str(success_count) + "/" + str(len(files))}
        )
        
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        logger.exception("Multi-file conversion failed")
        raise HTTPException(status_code=500, detail=str(e))
