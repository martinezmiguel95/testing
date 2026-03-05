from myapp.state import RagState

def topk_node(state: RagState, k=3) -> RagState:
    chunks = state.get("retrieved_chunks", [])

    top =sorted(chunks, key=lambda x: x.get("scores") or x.get("metadata", {}).get("score") or 0.0, reverse=True)[:k]
    state["final_chunks"] = top 
    return state