import pytest
import os
from unittest.mock import mock_open, patch
from src.adapters.driven.fs_adapter import LocalFileSystemAdapter

def test_fs_read_file_success():
    adapter = LocalFileSystemAdapter()
    
    # We patch builtins.open. Be careful with side effects
    with patch("builtins.open", mock_open(read_data="content")):
        with patch("os.path.exists", return_value=True):
             content = adapter.read_file("test.md")
             assert content == "content"

def test_fs_read_file_not_found():
    adapter = LocalFileSystemAdapter()
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            adapter.read_file("missing.md")

def test_fs_write_file():
    adapter = LocalFileSystemAdapter()
    with patch("builtins.open", mock_open()) as mock_file:
        path = adapter.save_file("test.pdf", b"data")
        assert os.path.isabs(path)
