from __future__ import annotations

import hashlib

import pymupdf


class PDFProcessingError(ValueError):
    """Raised when a PDF cannot be safely opened or read."""


def document_id(pdf_bytes: bytes) -> str:
    """Return a stable, session-local identifier for a PDF's contents."""
    return hashlib.sha256(pdf_bytes).hexdigest()


def extract_pdf_text(pdf_bytes: bytes) -> tuple[str, int]:
    """Extract selectable text from a PDF without writing it to disk."""
    if not pdf_bytes:
        raise PDFProcessingError("This file is empty.")

    try:
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as pdf:
            if pdf.needs_pass:
                raise PDFProcessingError(
                    "This PDF is password-protected. Upload an unlocked copy."
                )

            page_text: list[str] = []
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()
                if text:
                    page_text.append(f"--- Page {page_number} ---\n{text}")

            return "\n\n".join(page_text), pdf.page_count
    except PDFProcessingError:
        raise
    except Exception as error:
        raise PDFProcessingError(
            "This file could not be read as a PDF. Check the file and try again."
        ) from error
