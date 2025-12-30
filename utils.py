import logging
import re
from typing import List



# -----------------------
# Logger Setup
# -----------------------

def setup_logger(name: str = "agentic_news_verifier") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# -----------------------
# Text Utilities
# -----------------------

def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def split_sentences(text: str) -> List[str]:
    return [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]