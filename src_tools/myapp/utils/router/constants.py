#ROUTER_MODEL_ID = "anthropic.claude-3-haiku-20240307"
ROUTER_MODEL_ID = "gpt-4o-mini"
ROUTER_TEMPERATURE = 0

HIGH = 0.75              
MARGIN = 0.20             
MIN_SCORE = 0.30

TOP_K_kbs = 4

ALLOWED = {"single", "complex_direct", "complex_decompose", "none"}

ROUTER_PROMPT = [
    (
        "system",
        (
            "You are a strict routing controller. Return ONLY JSON with keys: strategy and choices.\n"
            "strategy ∈ {single, complex_direct, complex_decompose, none}.\n"
            f"choices must be a subset of the provided candidates.\n"
            "Pick one of the strategies using the rules:\n"
            "- Prefer 'single' when a single candidate is clearly dominant or the question pertains to one domain.\n"
            "- Use 'complex_direct' when two or more candidates are relevant and the query requires aggregating information directly from multiple KBs.\n"
            "- Use 'complex_decompose' when the question is multi-faceted and benefits from per-KB sub-queries.\n"
            "- Use 'none' only if none of the candidates seem relevant.\n"
            "Respond with compact JSON only."
        ),
    ),
    (
        "human",
        (
            "Question:\n{question}\n\n"
            "Candidates (subset only; do not propose any others):\n"
            "{candidates_json}\n\n"
            "Return JSON: {\"strategy\": <one of [single, complex_direct, complex_decompose, none]>, "
            "\"choices\": [<kb ids from candidates>]}"
        ),
    ),
]