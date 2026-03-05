from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json
from myapp.kb_data import KB_REGISTRY
from myapp.state import RagState
from myapp.utils.decomposer.constants import DECOMPOSER_PROMPT, DECOMPOSER_MODEL_ID, DECOMPOSER_TEMPERATURE
from myapp.utils.decomposer.decomposer_func import create_kb_candidates_small

llm = ChatOpenAI(model=DECOMPOSER_MODEL_ID, temperature=DECOMPOSER_TEMPERATURE)

PROMPT = ChatPromptTemplate.from_messages(DECOMPOSER_PROMPT)

def decompose_query(state: RagState) -> RagState:
    """
    Function tool focused on decompose a initial query in subqueries to improve the relation
    with the possible Knowledge Bases (KBs) available. The action is based on the relevance of each 
    knowledge base in comparison with the possible subqueries extracted.

    Arguments:
    - query (str): The initial user query.
    - kbs (dict): Mapping of KB name -> short description. Example:
        {
          "products": "Product specs, release notes, and compatibility",
          "support": "Troubleshooting, runbooks, and SLAs"
        }

    Returns:
    - dict with shape:
        {
          "subqueries": [
            {"kb": "<kb_name>", "query": "<focused subquery>"},
            ...
          ]
        }
    """


    print(f"I AM THE DECOMPOSER")

    msg = PROMPT | llm
    query = state["messages"][-1].content
    kb_candidates = create_kb_candidates_small(kb_registry=KB_REGISTRY)
    raw = msg.invoke({"query": query, "candidates_json": kb_candidates}).content

    print(f"Response for the decomposer: {raw}")

    try:
        data = json.loads(raw)
    except Exception as e:
        raise SyntaxError(f"Error generating the subqueries: {e}")
    
#    subqs = data.get("subqueries", [])
    print(f"SUBQUERIES: {data}")
    if not isinstance(data, dict):
        data = {}
    valid_kbs = set(KB_REGISTRY.keys())
    clean = []
    for q, kb in data.items():
        if isinstance(kb, str) and kb in valid_kbs and isinstance(q, str) and q.strip():
            clean.append({"kb": kb, "query": q.strip()})
            
    print(f"SUBQUERIES: {clean}")

    return {"subqueries": clean}
