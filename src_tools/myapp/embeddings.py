from typing import Dict, List, Optional, Tuple
import numpy as np
import faiss

from myapp.utils.embeddings.chunking import chunk_doc
from myapp.utils.embeddings.constants import DEFAULT_CHUNK_OVERLAP, DEFAULT_CHUNK_SIZE
from myapp.utils.embeddings.model import get_emb_model

class KBIndex:
    def __init__(self, kb_name: str, docs: List[Dict[str, str]], 
                 chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_overlap: int = DEFAULT_CHUNK_OVERLAP):
        self.kb_name = kb_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

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

        model = get_emb_model()
        emb = model.encode(texts, normalize_embeddings=True)
        self.emb = np.array(emb, dtype="float32")
        dim = self.emb.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(self.emb)

    def search(self, query: str, top_k: int = 5) -> List[dict]:
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
            meta.update({"rank": rank, "score": float(score), "index": int(i)})
            results.append({"page_content": text, "metadata": meta})
        return results

    @classmethod
    def from_storage(cls, kb_name: str, payload: Dict[str, object]) -> "KBIndex":
        obj = object.__new__(cls)
        obj.kb_name = kb_name
        obj.texts = payload["texts"]
        obj.emb = payload["emb"]
        obj.index = payload["index"]
        meta_rows = payload.get("meta_rows")
        if meta_rows is None:
            obj.meta_rows = [
                {"__kb": kb_name, "__doc": None, "__chunk_id": i, "span": (0, len(obj.texts[i]))}
                for i in range(len(obj.texts))
            ]
        else:
            obj.meta_rows = meta_rows
        # defaults if needed
        obj.chunk_size = None
        obj.chunk_overlap = 0
        return obj