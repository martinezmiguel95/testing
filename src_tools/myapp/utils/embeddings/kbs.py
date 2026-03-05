# kb.py
from typing import Dict, List
import threading

from myapp.embeddings import KBIndex
from myapp.utils.embeddings.storage import load_index, save_index

_KB_INDEXES: Dict[str, KBIndex] = {}
_KB_INDEXES_LOCK = threading.Lock()

def get_kb_index(kb_name: str, docs: List[Dict[str, str]]) -> KBIndex:
    idx = _KB_INDEXES.get(kb_name)
    if idx is not None:
        return idx

    with _KB_INDEXES_LOCK:
        idx = _KB_INDEXES.get(kb_name)
        if idx is not None:
            return idx

        loaded = load_index(kb_name)
        if loaded is not None:
            built = KBIndex.from_storage(kb_name, loaded)
            _KB_INDEXES[kb_name] = built
            return built

        built = KBIndex(kb_name, docs)
        save_index(kb_name, built.index, built.emb, built.texts, built.meta_rows)
        _KB_INDEXES[kb_name] = built
        return built