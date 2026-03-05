import os

# Keep if used elsewhere; local retrieval doesn’t require AWS.
AWS_REGION = os.getenv("AWS_REGION", "eu-west-3")

# LLM configs
SYNTH_MODEL_ID = "gpt-4o-mini"
#SYNTH_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
SYNTH_TEMPERATURE = 0
DEFAULT_CHUNK_SIZE = 200   
DEFAULT_CHUNK_OVERLAP = 20

# Embedding model
EMB_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Retrieval defaults
TOP_K_chunks = 3