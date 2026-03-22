import pdfplumber
import pytesseract
from pdf2image import convert_from_path


def load_pdf_text(pdf_path: str) -> str:
    """Extract text from PDF. Falls back to OCR for scanned/image-based PDFs."""
    # Try direct text extraction first
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

    if text_parts:
        return "\n".join(text_parts).strip()

    # Fallback: OCR via tesseract
    images = convert_from_path(pdf_path, dpi=300)
    ocr_parts = [pytesseract.image_to_string(img) for img in images]
    return "\n".join(ocr_parts).strip()
