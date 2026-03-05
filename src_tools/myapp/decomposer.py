from langchain_openai import ChatOpenAI
from myapp.utils.router.constants import ROUTER_MODEL_ID, ROUTER_TEMPERATURE
from langchain_core.prompts import ChatPromptTemplate
import json
from myapp.kb_data import KB_REGISTRY
from myapp.state import RagState

llm = ChatOpenAI(model=ROUTER_MODEL_ID, temperature=ROUTER_TEMPERATURE)

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a decomposer that base on a human query and a dictionary of possible Knowledges bases (KBs) from which extract information to respond, create subqueries mapped specific KBs."
     + "For that goal step by step reason and analyze the relevance of each KB with the query and try to find the best way to divide the initial query in subqueries to maximize the relevance between subquery - KB.\n"
     + "ONLY return a JSON with the list of the appropiate subqueries following this format:\n"
     + "{{subquery}}:{{KB}}"
     + "Knowledge Bases:\n" + "\n".join([f"- {k}: {desc}" for k, (_, desc) in KB_REGISTRY.items()])),
    ("human", "{query}")
])

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
    raw = msg.invoke({"query": query}).content

    query = state["messages"][-1].content

    print(f"Response for the decomposer: {raw}")

    try:
        data = json.loads(raw)
    except Exception as e:
        raise SyntaxError(f"Error generating the subqueries: {e}")
    
    # Validate shape and KB names
    subqs = data.get("subqueries", [])
    if not isinstance(subqs, list):
        subqs = []
    valid_kbs = set(KB_REGISTRY.keys())
    clean = []
    for item in subqs:
        kb = item.get("kb")
        q = item.get("query")
        if isinstance(kb, str) and kb in valid_kbs and isinstance(q, str) and q.strip():
            clean.append({"kb": kb, "query": q.strip()})

    return {"subqueries": clean}
