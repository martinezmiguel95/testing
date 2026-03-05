# chunking.py
from typing import List, Optional, Tuple

def chunk_doc(text: str, chunk_size: Optional[int], overlap: int) -> List[Tuple[str, Tuple[int, int]]]:
    if chunk_size is None:
        return [(text, (0, len(text)))]
    chunks: List[Tuple[str, Tuple[int, int]]] = []
    n = len(text)
    start = 0
    while start < n:
        end = min(start + chunk_size, n)
        chunks.append((text[start:end], (start, end)))
        if end == n:
            break
        start = max(0, end - overlap)
    return chunks