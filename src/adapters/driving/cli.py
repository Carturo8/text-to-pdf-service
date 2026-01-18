import typer
import os
import sys
from typing import Optional
from src.adapters.driven.fs_adapter import LocalFileSystemAdapter
from src.adapters.driven.pdf_adapter import Xhtml2PdfAdapter
from src.application.service import ConversionService

app = typer.Typer(help="Hexagonal Text-to-PDF Converter CLI")

def get_service() -> ConversionService:
    # Manual Dependency Injection
    fs_adapter = LocalFileSystemAdapter()
    pdf_adapter = Xhtml2PdfAdapter()
    return ConversionService(pdf_adapter, fs_adapter)

@app.command()
def convert(
    input_path: str = typer.Argument(..., help="Path to the source file (.md or .txt)"),
    output_path: str = typer.Option(None, "--output", "-o", help="Path to the output PDF file. Defaults to input_filename.pdf"),
):
    """
    Convert a Markdown or Text file to PDF.
    """
    if not os.path.exists(input_path):
        typer.secho(f"Error: Input file '{input_path}' does not exist.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # Default output path
    if not output_path:
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}.pdf"

    service = get_service()
    
    try:
        typer.secho(f"Converting '{input_path}' to '{output_path}'...", fg=typer.colors.BLUE)
        result_path = service.convert_file(input_path, output_path)
        typer.secho(f"Success! PDF generated at: {result_path}", fg=typer.colors.GREEN, bold=True)
    except Exception as e:
        typer.secho(f"Error during conversion: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
