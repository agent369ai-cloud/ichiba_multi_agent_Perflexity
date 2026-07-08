"""One-off script to create the Pinecone index and load the support-doc corpus.

Run with: python scripts/seed_pinecone.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cohere
from pinecone import Pinecone, ServerlessSpec

from config import settings

DOCS = [
    {
        "doc_id": "POL-101",
        "locale": "jp",
        "category": "visibility_issue",
        "content": "Policy states that category mapping is required for product visibility in the JP marketplace. Listings without a valid category will not appear in search results.",
    },
    {
        "doc_id": "POL-205",
        "locale": "en",
        "category": "visibility_issue",
        "content": "Listings may not appear in search if indexing is delayed after a feed submission. Indexing typically completes within 24 hours of a successful feed upload.",
    },
    {
        "doc_id": "POL-210",
        "locale": "en",
        "category": "visibility_issue",
        "content": "Products with incomplete required attributes (title, category, brand, images) are automatically excluded from search indexing until the feed is corrected and resubmitted.",
    },
    {
        "doc_id": "POL-301",
        "locale": "en",
        "category": "campaign_issue",
        "content": "Campaigns are rejected during moderation if the promotional discount exceeds the maximum allowed percentage for the product category, or if creative assets violate content guidelines.",
    },
    {
        "doc_id": "POL-305",
        "locale": "en",
        "category": "campaign_issue",
        "content": "A rejected campaign can be resubmitted after addressing the moderation feedback. Resubmissions are reviewed within 2 business days.",
    },
    {
        "doc_id": "POL-401",
        "locale": "en",
        "category": "billing_issue",
        "content": "Billing disputes for marketplace fees must be raised within 30 days of the invoice date. Merchants can view itemized fee breakdowns in the billing dashboard.",
    },
    {
        "doc_id": "POL-405",
        "locale": "en",
        "category": "billing_issue",
        "content": "Failed payment attempts for seller fees will retry automatically up to 3 times over 7 days before the merchant account is placed on payment hold.",
    },
    {
        "doc_id": "POL-501",
        "locale": "en",
        "category": "general_support",
        "content": "Merchant support tickets are triaged by priority: account access and payment issues are treated as high priority with a 4-hour first-response target.",
    },
]


def main():
    if not settings.COHERE_API_KEY or not settings.PINECONE_API_KEY:
        raise SystemExit("COHERE_API_KEY and PINECONE_API_KEY must be set in .env")

    co = cohere.ClientV2(api_key=settings.COHERE_API_KEY)
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)

    existing = {idx["name"] for idx in pc.list_indexes()}
    if settings.PINECONE_INDEX_NAME not in existing:
        print(f"Creating index '{settings.PINECONE_INDEX_NAME}'...")
        pc.create_index(
            name=settings.PINECONE_INDEX_NAME,
            dimension=1024,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=settings.PINECONE_ENV),
        )
    else:
        print(f"Index '{settings.PINECONE_INDEX_NAME}' already exists.")

    index = pc.Index(settings.PINECONE_INDEX_NAME)

    texts = [doc["content"] for doc in DOCS]
    embeddings = co.embed(
        texts=texts,
        model=settings.COHERE_EMBED_MODEL,
        input_type="search_document",
        embedding_types=["float"],
    ).embeddings.float_

    vectors = [
        {
            "id": doc["doc_id"],
            "values": embedding,
            "metadata": {
                "content": doc["content"],
                "locale": doc["locale"],
                "category": doc["category"],
            },
        }
        for doc, embedding in zip(DOCS, embeddings)
    ]

    index.upsert(vectors=vectors)
    print(f"Upserted {len(vectors)} documents into '{settings.PINECONE_INDEX_NAME}'.")


if __name__ == "__main__":
    main()
