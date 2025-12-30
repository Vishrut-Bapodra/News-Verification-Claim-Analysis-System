import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from ddgs import DDGS
from config import HTTP_TIMEOUT, MAX_SOURCES_PER_CLAIM


# -----------------------
# HTML Content Cleaner
# -----------------------
def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = " ".join(p.get_text() for p in soup.find_all("p"))
    return text.strip()

# -----------------------
# Search query helper
# -----------------------

def build_search_queries(entities: dict, original_claim: str) -> list[str]:
    queries = []

    def safe(v):
        return v if isinstance(v, str) else None

    person = safe(entities.get("person"))
    location = safe(entities.get("location"))
    country = safe(entities.get("country"))
    event = safe(entities.get("event_type"))

    if person and country and event:
        queries.append(f"{person} {event} {country}")
    if location and event:
        queries.append(f"{location} {event}")
    if country and event:
        queries.append(f"{country} {event}")
    if person:
        queries.append(person)

    if not queries:
        queries.append(original_claim)

    return queries

# -----------------------
# Web Search Tool
# -----------------------
TIER_1_DOMAINS = ["reuters.com", "apnews.com", "bbc.com", "aljazeera.com"]
TIER_2_DOMAINS = ["thehindu.com", "indianexpress.com", "dhakatribune.com", "dawn.com"]

def classify_source(url: str) -> str:
    for d in TIER_1_DOMAINS:
        if d in url:
            return "tier_1"
    for d in TIER_2_DOMAINS:
        if d in url:
            return "tier_2"
    return "tier_3"



def search_web_expanded(query: str) -> List[Dict]:
    """
    Search DuckDuckGo for a SINGLE query string.
    Query expansion must happen outside this function.
    """
    results = []
    seen_urls = set()

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            url = r.get("href")
            if not url or url in seen_urls:
                continue

            seen_urls.add(url)

            results.append({
                "title": r.get("title"),
                "url": url,
                "snippet": r.get("body"),
                "tier": classify_source(url)
            })

    return results


# -----------------------
# Fetch URL Content
# -----------------------
def fetch_url(url: str) -> str:
    response = requests.get(url, timeout=HTTP_TIMEOUT)
    response.raise_for_status()
    return response.text
