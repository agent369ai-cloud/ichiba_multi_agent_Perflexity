from fastapi import FastAPI
from models import MerchantRequest, MerchantResponse, EvidenceItem
from graph_flow import build_graph
from config import settings

app = FastAPI(title=settings.APP_NAME)
compiled_graph = build_graph()

@app.get("/")
def health_check():
    return {"message": f"{settings.APP_NAME} is running"}

@app.post("/ask", response_model=MerchantResponse)
def ask_support(request: MerchantRequest):
    initial_state = {
        "merchant_id": request.merchant_id,
        "language": request.language,
        "query": request.query,
        "session_id": request.session_id or ""
    }

    result = compiled_graph.invoke(initial_state)

    evidence_items = [
        EvidenceItem(**item) for item in result.get("evidence", [])
    ]

    return MerchantResponse(
        merchant_id=request.merchant_id,
        query=request.query,
        route=result.get("route", "unknown"),
        plan=result.get("plan", []),
        evidence=evidence_items,
        final_answer=result.get("final_answer", result.get("draft_answer", "")),
        status="success" if result.get("approved", False) else "needs_review"
    )