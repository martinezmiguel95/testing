SYNTH_MODEL_ID = "gpt-4o-mini"
#SYNTH_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
SYNTH_TEMPERATURE = 0

ANSWER_PROMPT = [
    ("system",
     "You have to answer the human question using ONLY the provided context. "
     "Cite the sources inline as [KB: {{kb}} - {{doc}}: {{i}}] for each snippet you use. "
     "If the context is insufficient or is empty, do not invent the answer and simply respond 'I dont know the answer'."
     "Lastly, always end the reponse text asking if the user need more specific detail ot additional information about the topic."),
    ("human", "Question: {q}\n\nContext:\n{context}")
]