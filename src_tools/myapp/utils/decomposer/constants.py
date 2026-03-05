DECOMPOSER_MODEL_ID = "gpt-4o-mini"
DECOMPOSER_TEMPERATURE = 0

DECOMPOSER_PROMPT = [
    ("system",
     "You are a decomposer that base on a human query and a dictionary of possible Knowledges bases (KBs) from which extract information to respond, create subqueries mapped specific KBs."
     + "For that goal step by step reason and analyze the relevance of each KB with the query and try to find the best way to divide the initial query in subqueries to maximize the relevance between subquery - KB.\n"
     + "ONLY return a JSON with the list of the appropiate subqueries following this format:\n"
     + "{{subquery}}:{{KB}}"
     + "Knowledge Bases:\n"
     + "{candidates_json}\n\n"
     + "Example of output:\n"
     + "{{\"CAPA CA‑12 details\": \"manufacturing\",\"SKU P-100 technical specifications\": \"products\",\"Network Timeouts troubleshooting\": \"support\"}}"),
    ("human", "{query}")
]