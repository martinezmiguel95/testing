# storage.py
import os
import json
import numpy as np
import faiss
from typing import Dict, List, Optional

CACHE_DIR = os.path.join(".cache", "kb")
os.makedirs(CACHE_DIR, exist_ok=True)

def paths_for(kb_name: str, dir: str = CACHE_DIR) -> Dict[str, str]:
    base = os.path.join(dir, kb_name)
    return {
        "faiss": base + ".faiss",
        "emb": base + ".npy",
        "texts": base + ".texts",
        "meta": base + ".meta.json",  
    }

def save_index(kb_name: str, index, emb, texts: List[str], meta_rows: List[dict]) -> None:
    p = paths_for(kb_name)
    faiss.write_index(index, p["faiss"])
    np.save(p["emb"], emb)
    with open(p["texts"], "w", encoding="utf-8") as f:
        for t in texts:
            f.write(t.replace("\n", " ") + "\n")
    with open(p["meta"], "w", encoding="utf-8") as f:
        json.dump(meta_rows, f, ensure_ascii=False)

def load_index(kb_name: str) -> Optional[Dict[str, object]]:
    p = paths_for(kb_name)
    if not (os.path.exists(p["faiss"]) and os.path.exists(p["emb"]) and os.path.exists(p["texts"])):
        return None
    try:
        index = faiss.read_index(p["faiss"])
        emb = np.load(p["emb"])
        with open(p["texts"], "r", encoding="utf-8") as f:
            texts = [line.rstrip("\n") for line in f]
        meta_rows = None
        if os.path.exists(p["meta"]):
            with open(p["meta"], "r", encoding="utf-8") as f:
                meta_rows = json.load(f)
        return {"index": index, "emb": emb, "texts": texts, "meta_rows": meta_rows}
    except Exception:
        return None