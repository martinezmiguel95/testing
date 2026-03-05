from typing import Dict, List, Optional
import os
import threading

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from myapp.config import EMB_MODEL_NAME
from myapp.kb_data import TEXTS

# Where to store per-KB artifacts
CACHE_DIR = os.path.join(".cache", "kb")
os.makedirs(CACHE_DIR, exist_ok=True)

def _paths_for(kb_name: str) -> Dict[str, str]:
    base = os.path.join(CACHE_DIR, kb_name)
    return {
        "faiss": base + ".faiss",
        "emb": base + ".npy",
        "texts": base + ".texts",
    }

# Lazy model init
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
    def __init__(self, kb_name: str, texts: List[str], model: SentenceTransformer):
        self.kb_name = kb_name
        self.texts = texts
        emb = model.encode(texts, normalize_embeddings=True)
        self.emb = np.array(emb, dtype="float32")
        dim = self.emb.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(self.emb)

    def search(self, query: str, top_k: int = 3) -> List[dict]:
        model = get_emb_model()
        q = model.encode([query], normalize_embeddings=True)
        q_vec = np.array(q, dtype="float32")
        sims, idxs = self.index.search(q_vec, top_k)
        results: List[dict] = []
        for rank, (i, score) in enumerate(zip(idxs[0], sims[0]), start=1):
            if i < 0:
                continue
            text = self.texts[int(i)]
            results.append({
                "page_content": text,
                "metadata": {
                    "__kb": self.kb_name,
                    "rank": rank,
                    "score": float(score),
                    "index": int(i),
                }
            })
        return results


# In-memory registry (per process)
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

        # Rehydrate KBIndex without recomputing
        obj = object.__new__(KBIndex)
        obj.kb_name = kb_name
        obj.texts = texts
        obj.emb = emb
        obj.index = index
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

def get_kb_index(kb_name: str, texts: List[str]) -> KBIndex:
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

def preload_all():
    for kb, docs in TEXTS.items():
        get_kb_index(kb, docs)

def local_retrieve(kb: str, query: str, top_k: int = 3) -> List[dict]:
    idx = get_kb_index(kb, TEXTS[kb])
    return idx.search(query, top_k=top_k)