from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from myapp.state import RagState
from myapp.config import SYNTH_MODEL_ID, SYNTH_TEMPERATURE

#synt_llm = Bedrock(model_id=SYNTH_MODEL_ID, model_kwargs={"temperature": SYNTH_TEMPERATURE})
synt_llm = ChatOpenAI(model=SYNTH_MODEL_ID, temperature=SYNTH_TEMPERATURE)

ANSWER_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You have to answer the human question using ONLY the provided context. "
     "Cite the sources inline as [KB: {{kb}} - {{doc}}: {{i}}] for each snippet you use. "
     "If the context is insufficient or is empty, do not invent the answer and simply respond 'I dont know the answer'."
     "Lastly, always end the reponse text asking if the user need more specific detail ot additional information about the topic."),
    ("human", "Question: {q}\n\nContext:\n{context}")
])

def format_context(chunks: List[dict]) -> str:
    lines = []
    for ch in chunks:
        kb = ch.get("metadata", {}).get("__kb", "unknown")
        doc = ch.get("metadata", {}).get("__doc", "unknown")
        c_id = ch.get("metadata", {}).get("__chunk_id", "unknown")
        text = ch.get("page_content") or ch.get("content", {}).get("text", "")
        lines.append(f"[KB:{kb} - {doc}:{c_id}] \n{text.strip()}")
    return "\n".join(lines)

def synthesize(state: RagState) -> RagState:
    print(f"I AM THE SINTHESIZER")
    q = state["messages"][-1].content
    ctx = format_context(state.get("retrieved_chunks", []))
    print(f"CONTEXT: {ctx}")
    chain = ANSWER_PROMPT | synt_llm
    out = chain.invoke({"q": q, "context": ctx})
    state["final_answer"] = out.content
    return state