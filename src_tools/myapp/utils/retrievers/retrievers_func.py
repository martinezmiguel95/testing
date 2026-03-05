from myapp.kb_data import TEXTS
from myapp.utils.embeddings.kbs import get_kb_index
from myapp.utils.retrievers.constants import TOP_K_chunks
from typing import List
import asyncio
from concurrent.futures import ProcessPoolExecutor


PROCESS_POOL = ProcessPoolExecutor(max_workers=4)
SEMAPHORE = asyncio.Semaphore(8)

def _local_retrieve_wrapper(kb: str, query: str) -> List[dict]: 
    return local_retrieve(kb, query)

def local_retrieve(kb: str, query: str, top_k: int = TOP_K_chunks) -> List[dict]:
    idx = get_kb_index(kb, TEXTS[kb])
    if idx is None:
        return []
    results = idx.search(query, top_k=top_k)
    return results

async def one_kb(kb: str, query: str) -> List[dict]: 
    async with SEMAPHORE: 
        loop = asyncio.get_running_loop() 
        executor = ProcessPoolExecutor(max_workers=4) 
        docs = await loop.run_in_executor(
            executor, local_retrieve, kb, query) 
        return [{**d, "__kb": kb, "__query": query} for d in docs]