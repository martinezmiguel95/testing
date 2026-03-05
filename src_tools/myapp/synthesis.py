from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from myapp.state import RagState
from myapp.utils.synthesizer.constants import SYNTH_MODEL_ID, SYNTH_TEMPERATURE, ANSWER_PROMPT
from myapp.utils.synthesizer.context import format_context

#synt_llm = Bedrock(model_id=SYNTH_MODEL_ID, model_kwargs={"temperature": SYNTH_TEMPERATURE})
synt_llm = ChatOpenAI(model=SYNTH_MODEL_ID, temperature=SYNTH_TEMPERATURE)

ANSWER_PROMPT = ChatPromptTemplate.from_messages(ANSWER_PROMPT)

def synthesize(state: RagState) -> RagState:
    print(f"I AM THE SINTHESIZER")
    q = state["messages"][-1].content
    #ctx = format_context(state.get("retrieved_chunks", []))
    ctx = state["context"]
    print(f"CONTEXT: {ctx}")
    chain = ANSWER_PROMPT | synt_llm
    out = chain.invoke({"q": q, "context": ctx})
    state["final_answer"] = out.content
    return state