from typing import Dict, Optional, List
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from agents import (
    scrape_article,
    extract_claims,
    verify_claims,
    analyze_bias,
    generate_final_report
)



# ----------------------------
# Shared State
# ---------------------------

class VerificationState(BaseModel):
    article_url: str
    article_text: Optional[str] = None
    article_metadata: Optional[Dict] = None

    claims: Optional[List[str]] = None
    claim_verification_results: Optional[List[Dict]] = None

    bias_analysis: Optional[Dict] = None
    final_report: Optional[Dict] = None

    bias_analysis: Optional[Dict] = None
    final_report: Optional[Dict] = None

    error: Optional[str] = None

# -----------------------
# Building Workflow
# -----------------------

def build_workflow():
    graph = StateGraph(VerificationState)

    graph.add_node("scraper",scrape_article)
    graph.add_node("claim_extractor", extract_claims)
    graph.add_node("verifier", verify_claims)
    graph.add_node("bias_analyzer", analyze_bias)
    graph.add_node("finalizer", generate_final_report)

    graph.set_entry_point("scraper")

    graph.add_edge("scraper","claim_extractor")
    graph.add_edge("claim_extractor", "verifier")
    graph.add_edge("verifier", "bias_analyzer")
    graph.add_edge("bias_analyzer", "finalizer")
    graph.add_edge("finalizer", END)

    return graph.compile()


# -----------------------
# Running Workflow
# -----------------------

def run_workflow(article_url: str) -> Dict:
    workflow = build_workflow()

    initial_state = {
        "article_url": article_url
    }

    result = workflow.invoke(initial_state)

    # result is ALWAYS treated as a dict
    if isinstance(result, dict) and result.get("error"):
        return {
            "error": result.get("error")
        }

    # Extract final report safely
    final_report = result.get("final_report")

    if not final_report:
        return {
            "error": "Workflow completed but no final report was generated"
        }

    return final_report