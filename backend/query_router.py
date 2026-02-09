"""
Query Router
Decides category: ring / necklace / both
"""

# =========================
# KEYWORDS
# =========================

RING_KEYWORDS = {
    "ring", "engagement", "wedding ring", "band", "solitaire"
}

NECKLACE_KEYWORDS = {
    "necklace", "chain", "pendant", "locket"
}

# =========================
# ROUTER
# =========================

def route_query(query: str):
    q = query.lower()

    ring_match = any(k in q for k in RING_KEYWORDS)
    necklace_match = any(k in q for k in NECKLACE_KEYWORDS)

    if ring_match and necklace_match:
        category = "both"
    elif ring_match:
        category = "ring"
    elif necklace_match:
        category = "necklace"
    else:
        category = "both"

    return {
        "category": category,
        "query": query
    }
