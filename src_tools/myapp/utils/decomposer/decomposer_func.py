import json

def create_kb_candidates_small(kb_registry: dict):
    candidates_payload = []
    for kb, (_, desc) in kb_registry.items():
        candidates_payload.append(
            {"kb": kb, "short_desc": desc[:160]}
        )
    
    candidates_json = json.dumps(candidates_payload, ensure_ascii=False)
    return candidates_json