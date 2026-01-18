import os
from pathlib import Path
from src.domain.ports import FileSystemPort

class LocalFileSystemAdapter(FileSystemPort):
    def read_file(self, path: str) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def save_file(self, path: str, content: bytes) -> str:
        with open(path, "wb") as f:
            f.write(content)
        return os.path.abspath(path)

    def list_files(self, directory: str, extensions: list[str]) -> list[str]:
        path = Path(directory)
        if not path.exists():
            return []
        files = []
        for ext in extensions:
            files.extend([str(p) for p in path.glob(f"*{ext}")])
        return files
