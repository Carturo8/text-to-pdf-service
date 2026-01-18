import os
import re
import markdown
from xhtml2pdf import pisa
from src.domain.model import ConversionRequest, ConversionResult, SourceFormat
from src.domain.ports import PDFConverterPort

class Xhtml2PdfAdapter(PDFConverterPort):
    def __init__(self, css_path: str = None):
        self.css_path = css_path
        # CSS compatible with xhtml2pdf (ReportLab)
        self.default_css = """
        <style>
            @page {
                size: a4;
                margin: 2.5cm;
                @frame footer_frame {
                    -pdf-frame-content: footerContent;
                    bottom: 1cm;
                    margin-left: 2.5cm;
                    margin-right: 2.5cm;
                    height: 1cm;
                }
            }
            body {
                font-family: 'Helvetica', sans-serif;
                font-size: 11pt;
                line-height: 1.5;
                color: #000000; /* FORCE BLACK TEXT */
            }
            h1 { 
                font-size: 22pt; 
                color: #000000; 
                border-bottom: 2px solid #000000; 
                padding-bottom: 5px; 
                margin-top: 20px;
                margin-bottom: 15px;
            }
            h2 { 
                font-size: 16pt; 
                color: #000000; 
                margin-top: 18px; 
                margin-bottom: 10px;
                font-weight: bold;
            }
            h3 { 
                font-size: 14pt; 
                color: #000000; 
                font-weight: bold;
                margin-top: 15px;
                margin-bottom: 8px;
            }
            p {
                margin-bottom: 10px;
                text-align: justify;
            }
            code { 
                background-color: #f5f5f5; 
                font-family: 'Courier New', Courier, monospace; 
                color: #000000;
            }
            pre { 
                background-color: #f5f5f5; 
                padding: 10px; 
                border: 1px solid #cccccc; 
                margin-bottom: 15px;
            }
            ul, ol {
                display: block;
                margin-top: 5px;
                margin-bottom: 10px;
                margin-left: 20px;
                padding-left: 10px;
            }
            li {
                display: list-item; /* Restore bullets */
                margin-bottom: 5px;
                color: #000000;
                list-style-type: disc; 
            }
            table { 
                border: 1px solid #000000; 
                width: 100%; 
                border-collapse: collapse; 
                margin-bottom: 15px;
            }
            th { 
                background-color: #e0e0e0; 
                font-weight: bold; 
                padding: 8px; 
                border: 1px solid #000000; 
                color: #000000;
            }
            td { 
                padding: 8px; 
                border: 1px solid #000000; 
                color: #000000;
            }
        </style>
        """

    def _preprocess_markdown(self, text: str) -> str:
        """
        Pre-processes markdown text to ensure professional rendering.
        Specifically fixes lists not having preceding newlines which breaks parsing.
        """
        # Fix: Force double newline before lists that follow text
        # Pattern: looks for non-newline char, single newline, then list marker
        text = re.sub(r'([^\n])\n(\s*[*+-] )', r'\1\n\n\2', text)
        text = re.sub(r'([^\n])\n(\s*\d+\. )', r'\1\n\n\2', text)
        return text

    def convert(self, request: ConversionRequest, output_dir: str) -> ConversionResult:
        try:
            filename = request.output_filename or f"output_{int(request.created_at.timestamp())}.pdf"
            if not filename.endswith('.pdf'):
                filename += ".pdf"
            
            output_path = os.path.join(output_dir, filename)

            # Convert Content to HTML
            html_body = ""
            if request.source_format == SourceFormat.MARKDOWN:
                # Preprocess markdown content
                processed_content = self._preprocess_markdown(request.content)
                html_body = markdown.markdown(
                    processed_content,
                    extensions=['tables', 'fenced_code', 'codehilite']
                )
            else:
                html_body = f"<pre>{request.content}</pre>"

            # Full HTML
            full_html = f"""
            <html>
            <head>
                <meta charset="utf-8"/>
                {self.default_css}
            </head>
            <body>
                {html_body}
                <div id="footerContent" style="text-align:center;">
                    Page <pdf:pagenumber>
                </div>
            </body>
            </html>
            """

            # Generate PDF
            with open(output_path, "wb") as output_file:
                pisa_status = pisa.CreatePDF(
                    src=full_html,
                    dest=output_file
                )
            
            if pisa_status.err:
                 raise RuntimeError(f"PDF generation error: {pisa_status.err}")
                
            size = os.path.getsize(output_path)
            return ConversionResult(
                file_path=os.path.abspath(output_path),
                size_bytes=size,
                success=True
            )

        except Exception as e:
            return ConversionResult(
                file_path="",
                size_bytes=0,
                success=False,
                error_message=str(e),
                created_at=request.created_at # Keep original timestamp
            )
