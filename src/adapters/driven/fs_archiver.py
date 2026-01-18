"""
FileSystem Archiver - History Storage Adapter.

Stores conversion metadata for long-term project history WITHOUT copying files.
This is storage-efficient while preserving all structural metadata.
"""
import hashlib
import json
from datetime import datetime
from pathlib import Path
from src.domain.model import ConversionRequest, ConversionResult
from src.domain.ports import ArchiverPort
from src.infrastructure.logger import logger


class FileSystemArchiver(ArchiverPort):
    """
    Metadata-only archiver for conversion history.
    
    Stores JSON metadata for each conversion run including:
    - Timestamp, file info, content hash
    - Success/error status
    - Size metrics
    
    Does NOT store file copies (storage efficient).
    """
    
    def __init__(self, archive_dir: str = "data/archive"):
        self.archive_dir = Path(archive_dir)
        self.meta_dir = self.archive_dir / "metadata"
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        
    def _calculate_hash(self, content: str) -> str:
        """Generate SHA-256 hash of content for deduplication tracking."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def archive(self, request: ConversionRequest, result: ConversionResult) -> None:
        """
        Archive conversion metadata (not files) for history.
        
        Args:
            request: Original conversion request
            result: Conversion result with status
        """
        try:
            timestamp = datetime.now()
            content_hash = self._calculate_hash(request.content)
            run_id = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{content_hash[:8]}"
            
            # Metadata only - no file copies for storage efficiency
            meta = {
                "run_id": run_id,
                "timestamp": timestamp.isoformat(),
                "date": timestamp.strftime("%Y-%m-%d"),
                "time": timestamp.strftime("%H:%M:%S"),
                "original_filename": request.output_filename,
                "source_format": request.source_format.value,
                "input_size_bytes": len(request.content.encode('utf-8')),
                "output_size_bytes": result.size_bytes,
                "content_hash": content_hash,
                "success": result.success,
                "error": result.error_message,
                # Additional structural metrics
                "word_count": len(request.content.split()),
                "line_count": len(request.content.splitlines()),
                "char_count": len(request.content),
            }
            
            # Store in daily files for easier management
            daily_file = self.meta_dir / f"{timestamp.strftime('%Y-%m-%d')}.jsonl"
            
            with open(daily_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(meta) + '\n')
                
            logger.info(f"Archived conversion metadata: {run_id}")

        except Exception as e:
            logger.error(f"Failed to archive conversion: {e}")
            # Do NOT raise - archiving failures should not block main flow
