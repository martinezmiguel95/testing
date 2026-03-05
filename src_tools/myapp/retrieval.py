from typing import List
from myapp.state import RagState
from myapp.embeddings import get_kb_index
from myapp.kb_data import TEXTS
from myapp.config import TOP_K_chunks
import asyncio
from concurrent.futures import ProcessPoolExecutor

def local_retrieve(kb: str, query: str, top_k: int = TOP_K_chunks) -> List[dict]:
    idx = get_kb_index(kb, TEXTS[kb])
    if idx is None:
        return []
    return idx.search(query, top_k=top_k)

def retrieve_complex(state: RagState) -> RagState:
    query = state["messages"][-1].content
    merged: List[dict] = []
    for kb in (state.get("route_choices") or []):
        merged.extend(local_retrieve(kb, query, top_k=TOP_K_chunks))
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
    docs = local_retrieve(kb, query, top_k=TOP_K_chunks)
    return {"retrieved_chunks": [{**d, "__kb": kb} for d in docs]}

PROCESS_POOL = ProcessPoolExecutor(max_workers=4)
SEMAPHORE = asyncio.Semaphore(8)
_PROCESS_POOL = None 

def _get_executor(): 
    if _PROCESS_POOL is None: # Adjust max_workers to your CPU/throughput 
        _PROCESS_POOL = ProcessPoolExecutor(max_workers=4) 
        return _PROCESS_POOL

def _local_retrieve_wrapper(kb: str, query: str, top_k: int) -> List[dict]: 
    return local_retrieve(kb, query, top_k)

async def one_kb(kb: str, query: str) -> List[dict]: 
    async with SEMAPHORE: 
        loop = asyncio.get_running_loop() 
        executor = ProcessPoolExecutor(max_workers=4) 
        docs = await loop.run_in_executor(
            executor, _local_retrieve_wrapper, kb, query, TOP_K_chunks
            ) 
        return [{**d, "__kb": kb} for d in docs]

async def retrieve_complex_parallel(state: RagState) -> RagState:
    print(f"I AM THE RETRIEVER FOR COMPLEX QUERIES")
    kbs = state["route_choices"]
    if state.get("subqueries"):
        queries = state["subqueries"]
    query = state["messages"][-1].content
    if not kbs:
        return {"retrieved_chunks": []}
    
    queries = [{"kb": kb, "query": query} for kb in kbs]

    chunks_per_kb = await asyncio.gather(*(one_kb(item["kb"], item["query"]) for item in queries))
    merged = [c for chunk in chunks_per_kb for c in chunk]
    return {"retrieved_chunks": merged}

