import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# -----------------------
# OpenRouter LLM Config
# -----------------------

# API key for OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY is not set. "
        "Please add it to your .env file."
    )

# OpenRouter base URL (OpenAI-compatible)
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Default LLM model (can be changed without touching code)
# Examples:
# - qwen/qwen-2.5-72b-instruct
# - mistralai/mistral-7b-instruct
# - meta-llama/llama-3.1-70b-instruct
LLM_MODEL_NAME = os.getenv(
    "LLM_MODEL_NAME",
    "qwen/qwen-2.5-72b-instruct"
)

# Temperature kept low for factual reasoning
LLM_TEMPERATURE = 0.0


# -----------------------
# Verification Settings
# -----------------------

# Max external sources to fetch per claim
MAX_SOURCES_PER_CLAIM = 3

# Timeout for HTTP requests (seconds)
HTTP_TIMEOUT = 10


# -----------------------
# Trusted Domains (optional)
# -----------------------
# Can be used later to filter low-quality sources

TRUSTED_NEWS_DOMAINS = [
    "bbc.com",
    "reuters.com",
    "apnews.com",
    "theguardian.com",
    "nytimes.com",
    "economist.com"
]
