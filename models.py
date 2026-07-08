from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class MerchantRequest(BaseModel):
    merchant_id: str = Field(..., description="Unique merchant id")
    language: str = Field(default="en", description="jp or en")
    query: str = Field(..., min_length=3, description="Merchant support query")
    session_id: Optional[str] = Field(default=None)

class EvidenceItem(BaseModel):
    source: str
    source_type: str
    confidence: float
    content: str
    metadata: Dict[str, Any] = {}

class MerchantResponse(BaseModel):
    merchant_id: str
    query: str
    route: str
    plan: List[str]
    evidence: List[EvidenceItem]
    final_answer: str
    status: str = "success"