from typing import List, Dict, Any

def search_documents(query: str) -> List[Dict[str, Any]]:
    return [
        {
            "source": "azure_ai_search",
            "source_type": "document",
            "confidence": 0.91,
            "content": "Policy states that category mapping is required for product visibility in JP marketplace.",
            "metadata": {"doc_id": "POL-101", "locale": "jp"}
        },
        {
            "source": "azure_ai_search",
            "source_type": "document",
            "confidence": 0.87,
            "content": "Listings may not appear if indexing is delayed after feed submission.",
            "metadata": {"doc_id": "POL-205", "locale": "en"}
        }
    ]

def query_sql(merchant_id: str) -> List[Dict[str, Any]]:
    return [
        {
            "source": "postgresql",
            "source_type": "sql",
            "confidence": 0.97,
            "content": f"Merchant {merchant_id} listing status is pending_moderation and category is null.",
            "metadata": {"table": "merchant_listings", "row_id": 556}
        }
    ]

def call_listing_api(merchant_id: str) -> List[Dict[str, Any]]:
    return [
        {
            "source": "listing_status_api",
            "source_type": "api",
            "confidence": 0.93,
            "content": f"Last indexing job for merchant {merchant_id} failed due to incomplete feed attributes.",
            "metadata": {"timestamp": "2026-07-08T09:10:00Z"}
        }
    ]

def load_memory(session_id: str | None) -> List[Dict[str, Any]]:
    if not session_id:
        return []
    return [
        {
            "source": "memory_store",
            "source_type": "memory",
            "confidence": 0.79,
            "content": "Merchant previously reported feed upload issue yesterday.",
            "metadata": {"session_id": session_id}
        }
    ]