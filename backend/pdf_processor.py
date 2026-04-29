"""
PDF text extraction and cleaning module.
"""

import pdfplumber
import re
import io


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract and clean text from a PDF file provided as bytes.
    Returns cleaned, readable text.
    """
    text_parts = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

    raw_text = "\n\n".join(text_parts)
    return clean_text(raw_text)


def clean_text(text: str) -> str:
    """Clean extracted text: normalize whitespace, remove artifacts."""
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove page numbers like "Page 1 of 5"
    text = re.sub(r'Page\s+\d+\s+(of\s+\d+)?', '', text, flags=re.IGNORECASE)
    # Normalize spaces
    text = re.sub(r'[ \t]+', ' ', text)
    # Strip leading/trailing whitespace from lines
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    return text.strip()
