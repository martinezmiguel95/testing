from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json
from myapp.kb_data import KB_REGISTRY
from myapp.state import RagState
from myapp.utils.judge.constants import JUDGE_PROMPT, JUDGE_MODEL_ID, JUDGE_TEMPERATURE
from myapp.utils.decomposer.decomposer_func import create_kb_candidates_small
from myapp.utils.synthesizer.context import format_context

llm = ChatOpenAI(model=JUDGE_MODEL_ID, temperature=JUDGE_TEMPERATURE)

PROMPT = ChatPromptTemplate.from_messages(JUDGE_PROMPT)

MAX_ROUTER_RETRIES = 3

def judge_node(state: RagState) -> RagState:

    print(f"I AM THE JUDGE")
    judge_retries = state.get("retries", 0)
    
    if judge_retries >= MAX_ROUTER_RETRIES:
        evaluation = {"verdict": "continue"}
        return evaluation
    
    context = format_context(state.get("retrieved_chunks", []))

    msg = PROMPT | llm
    query = state["messages"][-1].content
    raw = msg.invoke({"query": query, "context": context}).content

    print(f"Response for the JUDGE: {raw}")

    try:
        data = json.loads(raw)
    except Exception as e:
        raise SyntaxError(f"Error generating the evaluation: {e}")

    return {"evaluation": data, "context": context}
