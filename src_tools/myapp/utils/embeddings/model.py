# embeddings.py
from typing import Optional
import threading
from sentence_transformers import SentenceTransformer
from myapp.utils.embeddings.constants import EMB_MODEL_NAME

_emb_model: Optional[SentenceTransformer] = None
_emb_model_lock = threading.Lock()

def get_emb_model() -> SentenceTransformer:
    global _emb_model
    if _emb_model is None:
        with _emb_model_lock:
            if _emb_model is None:
                _emb_model = SentenceTransformer(EMB_MODEL_NAME)
    return _emb_model