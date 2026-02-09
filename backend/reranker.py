"""
Cross-encoder reranker for jewellery RAG
Final accuracy refinement step
"""

from sentence_transformers import CrossEncoder

# =========================
# CONFIG
# =========================

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
TOP_K = 10

# =========================
# LOAD MODEL
# =========================

reranker_model = CrossEncoder(MODEL_NAME)

# =========================
# HELPERS
# =========================

def metadata_to_text(metadata):
    return (
        f"Category: {metadata.get('category', '')}. "
        f"Material: {metadata.get('material', '')}. "
        f"Stone type: {metadata.get('stone_type', '')}. "
        f"Stone shape: {metadata.get('stone_shape', '')}. "
        f"Color: {metadata.get('color', '')}. "
        f"Description: {metadata.get('short_description', '')}."
    )

# =========================
# RERANK
# =========================

def rerank(query, candidates, top_k=TOP_K):
    if not candidates:
        return []

    pairs = []
    for c in candidates:
        text = metadata_to_text(c["metadata"])
        pairs.append((query, text))

    scores = reranker_model.predict(pairs)

    for c, s in zip(candidates, scores):
        c["rerank_score"] = float(s)

    candidates.sort(key=lambda x: x["rerank_score"], reverse=True)

    return candidates[:top_k]
