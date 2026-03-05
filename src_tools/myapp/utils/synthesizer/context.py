from typing import List

def format_context(chunks: List[dict]) -> str:
    lines = []
    for ch in chunks:
        kb = ch.get("metadata", {}).get("__kb", "unknown")
        doc = ch.get("metadata", {}).get("__doc", "unknown")
        c_id = ch.get("metadata", {}).get("__chunk_id", "unknown")
        text = ch.get("page_content") or ch.get("content", {}).get("text", "")
        lines.append(f"[KB:{kb} - {doc}:{c_id}] \n{text.strip()}")
    return "\n".join(lines)