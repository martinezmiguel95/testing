from typing import Dict, List
import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer

from typing import Optional, Tuple
from myapp.config import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP, EMB_MODEL_NAME
import threading
import os 

CACHE_DIR = os.path.join(".cache", "kb")
os.makedirs(CACHE_DIR, exist_ok=True)

def chunk_doc(text: str, chunk_size: Optional[int], overlap: int) -> List[Tuple[str, Tuple[int, int]]]:
    """
    Split a text into overlapping chunks.
    Returns list of (chunk_text, (start_idx, end_idx)).
    If chunk_size is None, returns a single chunk (the whole text).
    """
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

def _paths_for(kb_name: str) -> Dict[str, str]:
    base = os.path.join(CACHE_DIR, kb_name)
    return {
        "faiss": base + ".faiss",
        "emb": base + ".npy",
        "texts": base + ".texts",
        "meta": base + ".meta.npy"
    }

_emb_model: Optional[SentenceTransformer] = None
_emb_model_lock = threading.Lock()

def get_emb_model() -> SentenceTransformer: 
    global _emb_model 
    if _emb_model is None: 
        with _emb_model_lock: 
            if _emb_model is None:
                _emb_model = SentenceTransformer(EMB_MODEL_NAME) 
    return _emb_model

class KBIndex:
    def __init__(
            self, 
            kb_name: str, 
            docs: List[Dict[str, str]], 
            model: SentenceTransformer,
            chunk_size: Optional[int] = DEFAULT_CHUNK_SIZE,
            chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
            ):
        
        self.kb_name = kb_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Prepare chunk texts and row-aligned metadata
        texts: List[str] = []
        meta_rows: List[Dict[str, object]] = []

        for doc in docs:
            doc_name = doc["name"]
            content = doc["page_content"]
            pieces = chunk_doc(content, chunk_size, chunk_overlap)
            for chunk_id, (chunk_text, span) in enumerate(pieces):
                texts.append(chunk_text)
                meta_rows.append({
                    "__kb": kb_name,
                    "__doc": doc_name,
                    "__chunk_id": chunk_id,
                    "span": span, 
                })

        self.texts = texts
        self.meta_rows = meta_rows
        emb = model.encode(texts, normalize_embeddings=True)
        self.emb = np.array(emb, dtype="float32")
        dim = self.emb.shape[1]
        self.index = faiss.IndexFlatIP(dim)  
        self.index.add(self.emb)

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        print(f"Searching for chunks")
        model = get_emb_model()
        q = model.encode([query], normalize_embeddings=True)
        q_vec = np.array(q, dtype="float32")
        sims, idxs = self.index.search(q_vec, top_k)
        results: List[dict] = []
        for rank, (i, score) in enumerate(zip(idxs[0], sims[0]), start=1):
            if i < 0:
                continue
            text = self.texts[int(i)]
            meta = dict(self.meta_rows[i])
            meta.update({
                "rank": rank,
                "score": float(score),
                "index": i,
            })
            results.append({
                "page_content": text,
                "metadata": meta
            })
        return results
    

_KB_INDEXES: Dict[str, KBIndex] = {}
_KB_INDEXES_LOCK = threading.Lock()

def _load_kb_from_disk(kb_name: str) -> Optional[KBIndex]:
    paths = _paths_for(kb_name)
    if not (os.path.exists(paths["faiss"]) and os.path.exists(paths["emb"]) and os.path.exists(paths["texts"])):
        return None
    try:
        index = faiss.read_index(paths["faiss"])
        emb = np.load(paths["emb"])
        with open(paths["texts"], "r", encoding="utf-8") as f:
            texts = [line.rstrip("\n") for line in f]
        with open(paths(["meta"]), "r", encoding="utf-8") as f:
            meta_rows = json.load(f)

        obj = object.__new__(KBIndex)
        obj.kb_name = kb_name
        obj.texts = texts
        obj.emb = emb
        obj.index = index
        obj.meta_rows = meta_rows if meta_rows is not None else [
            {"__kb": kb_name, "__doc": None, "__chunk_id": i, "span": (0, len(texts[i]))
             } 
             for i in range(len(texts))]
        return obj
    except Exception:
        return None
    
def _save_kb_to_disk(kb_name: str, idx: KBIndex) -> None:
    paths = _paths_for(kb_name)
    faiss.write_index(idx.index, paths["faiss"])
    np.save(paths["emb"], idx.emb)
    with open(paths["texts"], "w", encoding="utf-8") as f:
        for t in idx.texts:
            f.write(t.replace("\n", " ") + "\n")
    with open(paths["meta"], "w", encoding="utf-8") as f:
        json.dump(idx.meta_rows, f, ensure_ascii=False)

def get_kb_index(kb_name: str, texts: List[str]) -> KBIndex:

    print(f"Searching in KB: {kb_name}")

    # Try in-memory cache
    idx = _KB_INDEXES.get(kb_name)
    if idx is not None:
        return idx

    with _KB_INDEXES_LOCK:
        # Check again inside the lock
        idx = _KB_INDEXES.get(kb_name)
        if idx is not None:
            return idx

        # Try to load persisted index
        loaded = _load_kb_from_disk(kb_name)
        if loaded is not None:
            _KB_INDEXES[kb_name] = loaded
            return loaded

        # Build and persist
        model = get_emb_model()
        built = KBIndex(kb_name, texts, model)
        _save_kb_to_disk(kb_name, built)
        _KB_INDEXES[kb_name] = built
        return built
