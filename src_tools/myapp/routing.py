import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from myapp.kb_data import KB_REGISTRY
from myapp.state import RagState
from myapp.utils.router.constants import ROUTER_PROMPT, ALLOWED, ROUTER_MODEL_ID, ROUTER_TEMPERATURE
from myapp.utils.router.routing_func import score_kbs, single_decision, create_kb_candidates

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

router_llm = ChatOpenAI(model=ROUTER_MODEL_ID, temperature=ROUTER_TEMPERATURE)

ROUTER_PROMPT = ChatPromptTemplate.from_messages(ROUTER_PROMPT)


def router_node(state: RagState) -> RagState:
    if not state.get("messages"):
        return {"route_strategy": "none", "route_choices": []}
    
    question = state["messages"][-1].content
    ranked = score_kbs(question, kb_registry=KB_REGISTRY)
      
    print(f"Scores of KBs: {ranked}")
    
    kb_selected = single_decision(ranked = ranked)
    
    if kb_selected:
        return {"route_strategy": "single", "route_choices": [kb_selected]}
    
    candidates_json = create_kb_candidates(data=ranked, kb_registry=KB_REGISTRY)
        
    msg = ROUTER_PROMPT | router_llm
    raw = msg.invoke({"question": question, "candidates_json": candidates_json}).content

    print(f"RESPONSE FROM ROUTER: {raw}")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        fallback = [kb for kb, _ in ranked[: min(2, len(ranked))]]
        return {"route_strategy": "complex_direct", "route_choices": fallback}

    strategy = str(data.get("strategy", "none")).lower()
    
    if strategy not in ALLOWED:
        strategy = "none"
    
    candidate_set = {kb for kb, _ in ranked}
    llm_choices = [c for c in (data.get("choices") or []) if c in candidate_set]

    if strategy == "single" and not llm_choices:
        strategy = "none"

    if strategy in {"complex_direct", "complex_decompose"} and not llm_choices:
        llm_choices = [kb for kb, _ in ranked[: min(2, len(ranked))]]

    return {"route_strategy": strategy, "route_choices": llm_choices}

