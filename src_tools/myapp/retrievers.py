from typing import List
from myapp.state import RagState
import asyncio
from myapp.utils.retrievers.retrievers_func import one_kb, local_retrieve

def retrieve_complex(state: RagState) -> RagState:
    query = state["messages"][-1].content
    merged: List[dict] = []
    for kb in (state.get("route_choices") or []):
        merged.extend(local_retrieve(kb, query))
    state["retrieved_chunks"] = merged
    return state

def retrieve_single(state: RagState) -> RagState:
    print(f"I AM THE RETRIEVER FOR SIMPLE QUERIES")
    choices = state["route_choices"]
    if not choices:
        state["retrieved_chunks"] = []
        return state
    kb = choices[0]
    query = state["messages"][-1].content
    docs = local_retrieve(kb, query)
    return {"retrieved_chunks": [{**d, "__kb": kb} for d in docs]}

#PROCESS_POOL = ProcessPoolExecutor(max_workers=4)
#SEMAPHORE = asyncio.Semaphore(8)
#_PROCESS_POOL = None 

#def _get_executor(): 
#    if _PROCESS_POOL is None: # Adjust max_workers to your CPU/throughput 
#        _PROCESS_POOL = ProcessPoolExecutor(max_workers=4) 
#        return _PROCESS_POOL

#def _local_retrieve_wrapper(kb: str, query: str, top_k: int) -> List[dict]: 
#    return local_retrieve(kb, query, top_k)

async def retrieve_complex_parallel(state: RagState) -> RagState:
    print(f"I AM THE RETRIEVER FOR COMPLEX QUERIES")
    kbs = state["route_choices"]
    query = state["messages"][-1].content
    queries = [{"query": query, "kb": kb,} for kb in kbs]
    if state.get("subqueries"):
        queries = state["subqueries"]

    if not kbs:
        return {"retrieved_chunks": []}


    chunks_per_kb = await asyncio.gather(*(one_kb(item["kb"], item["query"]) for item in queries))
    merged = [c for chunk in chunks_per_kb for c in chunk]
    print("MERGED: {merged}")
    return {"retrieved_chunks": merged}

