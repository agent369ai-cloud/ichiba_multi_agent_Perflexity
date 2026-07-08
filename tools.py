
from typing import List, Dict, Any

import cohere
from pinecone import Pinecone

from config import settings

_cohere_client = cohere.ClientV2(api_key=settings.COHERE_API_KEY) if settings.COHERE_API_KEY else None
_pinecone_index = (
    Pinecone(api_key=settings.PINECONE_API_KEY).Index(settings.PINECONE_INDEX_NAME)
    if settings.PINECONE_API_KEY
    else None
)

_FALLBACK_DOCS = [
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

def search_documents(query: str) -> List[Dict[str, Any]]:
    if not _cohere_client or not _pinecone_index:
        return _FALLBACK_DOCS

    try:
        embedding = _cohere_client.embed(
            texts=[query],
            model=settings.COHERE_EMBED_MODEL,
            input_type="search_query",
            embedding_types=["float"],
        ).embeddings.float_[0]

        matches = _pinecone_index.query(
            vector=embedding, top_k=3, include_metadata=True
        ).matches

        return [
            {
                "source": "pinecone",
                "source_type": "document",
                "confidence": round(match.score, 4),
                "content": match.metadata["content"],
                "metadata": {
                    "doc_id": match.id,
                    "locale": match.metadata.get("locale"),
                    "category": match.metadata.get("category"),
                },
            }
            for match in matches
        ]
    except Exception:
        return _FALLBACK_DOCS

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