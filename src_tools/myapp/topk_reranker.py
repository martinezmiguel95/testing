from myapp.state import RagState

def get_score(ch: dict) -> float:
    # If "scores" can be a list or a single float, normalize
    s = ch.get("scores")
    if isinstance(s, (int, float)):
        return float(s)
    if isinstance(s, (list, tuple)) and s:
        try:
            return float(s[0])
        except Exception:
            pass
    return float(ch.get("metadata", {}).get("score", 0.0))

def topk_node(state: RagState, k=2) -> RagState:
    chunks = state.get("retrieved_chunks", [])

    groups = {}
    order = []  # to preserve first-seen query order
    for ch in chunks:
        meta = ch.get("metadata", {}) or {}
        q = meta.get("query")  # adjust if your key differs, e.g., "__query"
        if q is None:
            # Place chunks without a query into a special group
            q = "__NO_QUERY__"
        if q not in groups:
            groups[q] = []
            order.append(q)
        groups[q].append(ch)

    # For each query, take top-k by score
    final = []
    for q in order:
        group = groups[q]
        topk = sorted(group, key=get_score, reverse=True)[:k]
        final.extend(topk)

    state["final_chunks"] = final
    return state