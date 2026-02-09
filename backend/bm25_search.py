"""
Category-aware BM25 search
Ring → ring only
Necklace → necklace only
Both → merge results
"""

import pickle
from pathlib import Path

import nltk
from nltk.tokenize import word_tokenize

# =========================
# CONFIG
# =========================

BM25_DIR = Path("bm25")
TOP_K = 10

# =========================
# LOAD INDEXES
# =========================

def load_bm25(category):
    with open(BM25_DIR / f"{category}_bm25.pkl", "rb") as f:
        data = pickle.load(f)
    return data["bm25"], data["id_map"]

bm25_ring, ring_map = load_bm25("ring")
bm25_necklace, necklace_map = load_bm25("necklace")

# =========================
# SEARCH
# =========================

def bm25_search(query, category="both", top_k=TOP_K):
    tokens = word_tokenize(query.lower())
    results = []

    if category in ("ring", "both"):
        scores = bm25_ring.get_scores(tokens)
        for idx in sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]:
            results.append({
                "score": float(scores[idx]),
                "category": "ring",
                "metadata": ring_map[idx]
            })

    if category in ("necklace", "both"):
        scores = bm25_necklace.get_scores(tokens)
        for idx in sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]:
            results.append({
                "score": float(scores[idx]),
                "category": "necklace",
                "metadata": necklace_map[idx]
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
