import os
from typing import List
from pypdf import PdfReader
from docx import Document

def load_document(path: str) -> List[str]:
    """
    Load text from a file. Supports .txt, .pdf, .docx.
    Returns a list of non-empty text chunks (e.g., pages or paragraphs).
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        return _load_txt(path)
    elif ext == ".pdf":
        return _load_pdf(path)
    elif ext == ".docx":
        return _load_docx(path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

def _load_txt(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # Simple chunking by double newline
    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
    return chunks

def _load_pdf(path: str) -> List[str]:
    reader = PdfReader(path)
    chunks = []
    for page in reader.pages:
        text = page.extract_text()
        if text and text.strip():
            chunks.append(text.strip())
    return chunks

def _load_docx(path: str) -> List[str]:
    doc = Document(path)
    chunks = []
    # Chunk by paragraph
    for para in doc.paragraphs:
        if para.text and para.text.strip():
            chunks.append(para.text.strip())
    return chunks
