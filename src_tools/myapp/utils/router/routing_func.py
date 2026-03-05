from myapp.embeddings import get_emb_model
from typing import Dict, Tuple, List, Optional
import numpy as np
from myapp.utils.router.constants import HIGH, MARGIN, MIN_SCORE, TOP_K_kbs
import json

def create_kb_candidates(data: list, kb_registry: dict):
    candidates_payload = []
    for kb, score in data:
        desc = kb_registry.get(kb, (None, ""))[1]
        candidates_payload.append(
            {"kb": kb, "score": _round_score(score), "short_desc": desc}
        )
    
    candidates_json = json.dumps(candidates_payload, ensure_ascii=False)
    return candidates_json

def single_decision(ranked: list, high_threshold: int = HIGH, margin: int = MARGIN):
    res = None
    top1_kb, top1 = ranked[0]
    top2 = ranked[1][1] if len(ranked) > 1 else -1.0

    if (top1 >= high_threshold) or (top2 >= 0 and (top1 - top2) >= margin):
        res = top1_kb
        return res
    
    return res

def _prioritize_ranked( ranked: List[tuple], prioritize: Optional[List[str]] ) -> List[tuple]: 
    if not prioritize: 
        return ranked 
    priority = set(prioritize) 
    preferred = [(kb, score) for kb, score in ranked if kb in priority] 
    others = [(kb, score) for kb, score in ranked if kb not in priority]  
    return preferred + others

def _preload_kb_desc_embeddings(kb_registry: dict) -> None:
    kb_desc_emb: Dict[str, np.ndarray] = {}
    model = get_emb_model()
    for kb, (_, desc) in kb_registry.items():
        v = model.encode([desc], normalize_embeddings=True)[0].astype("float32")
        kb_desc_emb[kb] = v
    return kb_desc_emb
    
def score_kbs(question: str, kb_registry: dict, top_n: int = TOP_K_kbs) -> List[Tuple[str, float]]:
    kb_desc_emb = _preload_kb_desc_embeddings(kb_registry) 
    vq = get_emb_model().encode([question], normalize_embeddings=True)[0].astype("float32")
    scores = [(kb, float(np.dot(vq, kb_desc_emb[kb]))) for kb in kb_desc_emb]
    #print(scores)
    #scores = [ (kb, s) for kb, s in scores if s >= MIN_SCORE]
    print(scores)
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

def _round_score(x: float) -> float:
    return float(np.clip(np.round(x, 3), 0.0, 1.0))