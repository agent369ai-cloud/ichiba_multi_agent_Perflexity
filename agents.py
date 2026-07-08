from typing import Dict, Any, List

from tools import search_documents, query_sql, call_listing_api, load_memory

def router_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    query = state["query"].lower()

    if "visible" in query or "search" in query or "listing" in query:
        route = "visibility_issue"
    elif "campaign" in query or "rejected" in query:
        route = "campaign_issue"
    elif "payment" in query or "billing" in query:
        route = "billing_issue"
    else:
        route = "general_support"

    return {"route": route}

def planner_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    route = state["route"]

    if route == "visibility_issue":
        plan = [
            "load memory context",
            "search policy documents",
            "check merchant listing in SQL",
            "check indexing API status",
            "synthesize answer"
        ]
    elif route == "campaign_issue":
        plan = [
            "load memory context",
            "search campaign policy docs",
            "check campaign SQL records",
            "check moderation API",
            "synthesize answer"
        ]
    else:
        plan = [
            "load memory context",
            "search support docs",
            "synthesize answer"
        ]

    return {"plan": plan}

def memory_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    items = load_memory(state.get("session_id"))
    return {"memory_results": items}

def rag_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    docs = search_documents(state["query"])
    return {"doc_results": docs}

def sql_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    route = state["route"]
    if route in ["visibility_issue", "campaign_issue"]:
        rows = query_sql(state["merchant_id"])
    else:
        rows = []
    return {"sql_results": rows}

def api_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    route = state["route"]
    if route == "visibility_issue":
        api_results = call_listing_api(state["merchant_id"])
    else:
        api_results = []
    return {"api_results": api_results}

def synthesizer_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    evidence = []
    evidence.extend(state.get("memory_results", []))
    evidence.extend(state.get("doc_results", []))
    evidence.extend(state.get("sql_results", []))
    evidence.extend(state.get("api_results", []))

    answer_lines = [
        f"Merchant query: {state['query']}",
        f"Detected route: {state['route']}",
        "Root-cause analysis based on collected evidence:"
    ]

    for item in evidence:
        answer_lines.append(f"- [{item['source_type']}] {item['content']}")

    answer_lines.extend([
        "",
        "Recommended next steps:",
        "1. Update missing category mapping.",
        "2. Re-submit product feed with required attributes.",
        "3. Trigger re-indexing and verify status in merchant dashboard."
    ])

    return {
        "evidence": evidence,
        "draft_answer": "\n".join(answer_lines)
    }

def critic_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    draft = state.get("draft_answer", "")
    evidence = state.get("evidence", [])

    issues = []
    if len(evidence) == 0:
        issues.append("No evidence collected.")
    if "Recommended next steps" not in draft:
        issues.append("No actionable steps present.")

    approved = len(issues) == 0

    return {
        "approved": approved,
        "critic_issues": issues
    }

def guardrail_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    draft = state.get("draft_answer", "")
    safe_answer = draft.replace("internal_only", "[redacted]")
    return {"final_answer": safe_answer}