import os
from typing import List

CHUNK_SIZE = 800  # tokens, approx via chars/4
CHUNK_OVERLAP = 100


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks (rough token estimate: 1 token ~ 4 chars)."""
    char_size = chunk_size * 4
    char_overlap = overlap * 4
    chunks = []
    start = 0
    while start < len(text):
        end = start + char_size
        chunks.append(text[start:end])
        start = end - char_overlap
    return chunks


def extract_text(file_path: str) -> str:
    """Convert a supported doc (.txt for now) to raw text."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    raise ValueError(f"unsupported file type: {ext}")
