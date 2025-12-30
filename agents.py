import json
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tools import fetch_url, clean_html, search_web_expanded, build_search_queries
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, LLM_MODEL_NAME

# -----------------------
# LLM Setup
# -----------------------
llm = ChatOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    model=LLM_MODEL_NAME,
    temperature=0
)

# -----------------------
# Scraper Agent
# -----------------------
def scrape_article(state):
    html = fetch_url(state.article_url)
    state.article_text = clean_html(html)
    state.article_metadata = {"url": state.article_url}
    return state

# -----------------------
# Claim Extraction
# -----------------------
def extract_claims(state):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract clear factual claims as bullet points."),
        ("human", "{text}")
    ])

    response = llm.invoke(
        prompt.format_messages(text=state.article_text)
    )

    state.claims = [
        l.strip("- ").strip()
        for l in response.content.split("\n")
        if l.strip()
    ]
    return state

# -----------------------
# Entity Extraction
# -----------------------
def extract_search_entities(claim: str) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Return STRICT JSON with keys: person, location, country, event_type. "
         "Each value MUST be a single string or null. No arrays."),
        ("human", "{claim}")
    ])

    response = llm.invoke(prompt.format_messages(claim=claim))

    try:
        data = json.loads(response.content)
    except Exception:
        return {}

    def normalize(v):
        if isinstance(v, list):
            return " ".join(map(str, v))
        return v

    return {k: normalize(v) for k, v in data.items()}


# -----------------------
# Claim Verification
# -----------------------
def verify_claims(state):
    results = []

    for claim in state.claims:
        entities = extract_search_entities(claim)
        queries = build_search_queries(entities, claim)

        sources = []
        for q in queries:
            sources.extend(search_web_expanded(q))

        sources_text = "\n".join(
            f"- {s['title']} ({s['url']})"
            for s in sources
        ) or "No external sources found."

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Classify claim as supported, likely_supported, inconclusive, or contradicted."),
            ("human", "Claim: {claim}\nSources:\n{sources}")
        ])

        analysis = llm.invoke(
            prompt.format_messages(claim=claim, sources=sources_text)
        )

        results.append({
            "claim": claim,
            "analysis": analysis.content,
            "sources": sources
        })

    state.claim_verification_results = results
    return state

# -----------------------
# Bias Analysis
# -----------------------
def analyze_bias(state):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Analyze bias or sensational language."),
        ("human", "{text}")
    ])

    response = llm.invoke(
        prompt.format_messages(text=state.article_text)
    )

    state.bias_analysis = {"analysis": response.content}
    return state

# -----------------------
# Final Report
# -----------------------
def generate_final_report(state):
    claims_text = "\n".join(
        f"- {c['claim']}: {c['analysis']}"
        for c in state.claim_verification_results
    )

    bias_text = state.bias_analysis.get("analysis", "")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Provide final confidence score (0–100) with explanation."),
        ("human", "Claims:\n{claims}\n\nBias:\n{bias}")
    ])

    response = llm.invoke(
        prompt.format_messages(claims=claims_text, bias=bias_text)
    )

    state.final_report = {
        "article_url": state.article_metadata["url"],
        "claims": state.claim_verification_results,
        "bias_analysis": state.bias_analysis,
        "final_assessment": response.content
    }
    return state
