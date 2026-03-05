from langgraph.graph import StateGraph, START, END
from myapp.state import RagState
from myapp.routing import router_node
from myapp.topk_reranker import topk_node
from myapp.retrievers import retrieve_single, retrieve_complex_parallel
from myapp.synthesis import synthesize
from myapp.decomposer import decompose_query
from myapp.judge import judge_node
import operator


def routing(state: RagState) -> str:
    s = state["route_strategy"]
    if s == "complex_direct":
        return "retrieve_complex_parallel"
    elif s == "complex_decompose":
        return "decompose_query"
    elif s == "single": 
        return "retrieve_single"
    else:
        return "synthesize"
    
def evaluation(state: RagState) -> str:
    return state.get("evaluation", {}).get("verdict", "continue")

def build_app():
    graph = StateGraph(
        RagState,
        reducers={
            "messages": operator.add,
            "retrieved_chunks": operator.add
        }
                       )
    graph.add_node("router", router_node)
    graph.add_node("retrieve_single", retrieve_single)
    graph.add_node("retrieve_complex_parallel", retrieve_complex_parallel)
    graph.add_node("decompose_query", decompose_query)
    graph.add_node("topk_node", topk_node)
    graph.add_node("synthesize", synthesize)
    graph.add_node("judge", judge_node)

    graph.add_edge(START, "router")

    graph.add_conditional_edges( "router", routing, 
                                { "retrieve_complex_parallel": "retrieve_complex_parallel", 
                                 "decompose_query": "decompose_query", 
                                 "retrieve_single": "retrieve_single", 
                                 "synthesize": "synthesize", }, )
    graph.add_conditional_edges(
    "judge",
    evaluation,
    {
        "continue": "synthesize",
        "reevaluate": "router",
    },
)
    graph.add_edge("retrieve_single", "judge")
    graph.add_edge("decompose_query", "retrieve_complex_parallel")
    graph.add_edge("retrieve_complex_parallel", "topk_node")
    graph.add_edge("topk_node", "judge")
    graph.add_edge("synthesize", END)



    return graph.compile()