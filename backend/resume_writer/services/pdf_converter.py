import os
from docx2pdf import convert

class PDFConverter:
    @staticmethod
    def convert_to_pdf(docx_path: str, pdf_path: str = None) -> str:
        """
        Converts the finalized docx to PDF using Windows MS Word API (docx2pdf).
        Returns the absolute path to the PDF.
        """
        if not pdf_path:
            pdf_path = docx_path.replace(".docx", ".pdf")
            
        abs_docx = os.path.abspath(docx_path)
        abs_pdf = os.path.abspath(pdf_path)
        
        import sys
        if sys.platform == "win32":
            import pythoncom
            pythoncom.CoInitialize()
        
        try:
            convert(abs_docx, abs_pdf)
        finally:
            if sys.platform == "win32":
                pythoncom.CoUninitialize()
                
        return abs_pdf
