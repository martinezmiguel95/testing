import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from myapp.kb_data import KB_REGISTRY
from myapp.state import RagState
from myapp.utils.router.constants import ROUTER_PROMPT, ALLOWED, ROUTER_MODEL_ID, ROUTER_TEMPERATURE
from myapp.utils.router.routing_func import score_kbs, single_decision, create_kb_candidates,_prioritize_ranked

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

router_llm = ChatOpenAI(model=ROUTER_MODEL_ID, temperature=ROUTER_TEMPERATURE)

ROUTER_PROMPT = ChatPromptTemplate.from_messages(ROUTER_PROMPT)


def router_node(state: RagState) -> RagState:
    if not state.get("messages"):
        return {"route_strategy": "none", "route_choices": []}
    
    question = state["messages"][-1].content
    retries = state.get("retries", 0)
    evaluation = (state.get("evaluation") or {})
    verdict = str(evaluation.get("verdict", "continue")).lower()
    ranked = score_kbs(question, kb_registry=KB_REGISTRY)

    if not ranked:
        return {"route_strategy": "none", "route_choices": [], "subqueries": []}

# If judge asked for reevaluation, incorporate guidance
    if verdict == "reevaluate":
        suggested_subqueries = evaluation.get("suggested_subqueries") or []
        kbs_to_prioritize = evaluation.get("kbs_to_prioritize") or []

        # Reorder ranked with judged KBs first
        ranked = _prioritize_ranked(ranked, kbs_to_prioritize)

        # If previous attempt was single, broaden to complex; else keep complex
        prev_strategy = state.get("route_strategy", "none")
        if prev_strategy == "single":
            # Move to complex; prefer decompose if subqueries are present
            if suggested_subqueries:
                # Route to complex_decompose and pass subqueries
                choices = [kb for kb, _ in ranked[: min(3, len(ranked))]]
                return {
                "route_strategy": "complex_decompose",
                "route_choices": choices,
                "subqueries": suggested_subqueries,
                "judge_retries": retries + 1
                }
            else:
                choices = [kb for kb, _ in ranked[: min(2, len(ranked))]]
                return {
                "route_strategy": "complex_direct",
                "route_choices": choices,
                "subqueries": [],
                "judge_retries": retries + 1
                }
      
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

