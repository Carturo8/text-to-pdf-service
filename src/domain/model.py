from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Optional

class SourceFormat(str, Enum):
    MARKDOWN = "md"
    TEXT = "txt"

@dataclass
class ConversionRequest:
    content: str
    source_format: SourceFormat
    output_filename: str
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class ConversionResult:
    file_path: str
    size_bytes: int
    success: bool
    created_at: datetime = field(default_factory=datetime.now)
    error_message: Optional[str] = None
