from typing import List, Optional, Literal, TypedDict, Annotated
from langchain_core.messages import AnyMessage
import operator

class RagState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    route_strategy: Literal["single", "complex", "none"]
    route_choices: Optional[List[str]]
    retrieved_chunks: Annotated[List[dict], operator.add]
    subqueries: List[str]
    final_chunks: List[dict]
    context: Optional[str]
    final_answer: str
    evaluation: Optional[dict]
    retries: int
    citations: List[dict]
