from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.adapters.driving.api import app

client = TestClient(app)

def test_convert_success():
    # Helper to simulate file creation for response
    def mock_convert(inp, outp):
        # We assume the API logic creates outp. 
        # But we need it to exist for FileResponse
        with open(outp, 'wb') as f:
            f.write(b"pdf data")
        return outp

    with patch("src.adapters.driving.api.get_service") as mock_get_service:
        mock_service = MagicMock()
        mock_service.convert_file.side_effect = mock_convert
        mock_get_service.return_value = mock_service
        
        response = client.post(
            "/convert/",
            files={"file": ("test.md", b"# Content", "text/markdown")}
        )
        
        assert response.status_code == 200
        assert response.headers['content-type'] == 'application/pdf'

def test_convert_invalid_type():
    response = client.post(
        "/convert/",
        files={"file": ("test.exe", b"bin", "application/octet-stream")}
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()['detail']

def test_convert_service_error():
    with patch("src.adapters.driving.api.get_service") as mock_get_service:
        mock_service = MagicMock()
        mock_service.convert_file.side_effect = Exception("Service failed")
        mock_get_service.return_value = mock_service

        response = client.post(
             "/convert/",
            files={"file": ("test.md", b"# Content", "text/markdown")}
        )
        assert response.status_code == 500
