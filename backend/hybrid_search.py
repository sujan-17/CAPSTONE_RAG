"""
Hybrid retrieval: FAISS (dense) + BM25 (sparse)
Category-aware and accuracy-first
"""

import numpy as np

from faiss_search import encode_text, faiss_search
from bm25_search import bm25_search

# =========================
# CONFIG
# =========================

FAISS_WEIGHT = 0.7
BM25_WEIGHT = 0.3
TOP_K = 10

# =========================
# NORMALIZATION
# =========================

def min_max_normalize(scores):
    if not scores:
        return scores

    min_s = min(scores)
    max_s = max(scores)

    if max_s == min_s:
        return [1.0 for _ in scores]

    return [(s - min_s) / (max_s - min_s) for s in scores]

# =========================
# HYBRID SEARCH
# =========================

def hybrid_search(query, category="both", top_k=TOP_K):
    # ---- FAISS ----
    query_embedding = encode_text(query)
    faiss_results = faiss_search(query_embedding, category=category, top_k=top_k)

    faiss_scores = [r["score"] for r in faiss_results]
    faiss_norm = min_max_normalize(faiss_scores)

    faiss_dict = {}
    for r, s in zip(faiss_results, faiss_norm):
        faiss_dict[r["id"]] = {
            "score": s,
            "metadata": r["metadata"],
            "category": r["category"]
        }

    # ---- BM25 ----
    bm25_results = bm25_search(query, category=category, top_k=top_k)
    bm25_scores = [r["score"] for r in bm25_results]
    bm25_norm = min_max_normalize(bm25_scores)

    bm25_dict = {}
    for r, s in zip(bm25_results, bm25_norm):
        bm25_dict[r["metadata"]["id"]] = {
            "score": s,
            "metadata": r["metadata"],
            "category": r["category"]
        }

    # ---- FUSION ----
    fused = {}

    for k, v in faiss_dict.items():
        fused[k] = {
            "score": float(FAISS_WEIGHT * v["score"]),
            "metadata": v["metadata"],
            "category": v["category"]
        }

    for k, v in bm25_dict.items():
        if k in fused:
            fused[k]["score"] += float(BM25_WEIGHT * v["score"])
        else:
            fused[k] = {
                "score": BM25_WEIGHT * v["score"],
                "metadata": v["metadata"],
                "category": v["category"]
            }

    # ---- SORT ----
    results = sorted(
        fused.values(),
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]
