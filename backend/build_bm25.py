"""
Build BM25 corpus from jewellery metadata
Ring and Necklace handled separately
"""

import json
import pickle
from pathlib import Path

import nltk
from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi

# =========================
# CONFIG
# =========================

METADATA_DIR = Path("data/metadata")
OUTPUT_DIR = Path("bm25")

OUTPUT_DIR.mkdir(exist_ok=True)

FILES = {
    "ring": "ring_metadata.json",
    "necklace": "necklace_metadata.json"
}

# =========================
# HELPERS
# =========================

def metadata_to_text(item):
    fields = [
        item.get("category", ""),
        item.get("material", ""),
        item.get("stone_type", ""),
        item.get("stone_shape", ""),
        item.get("color", ""),
        item.get("short_description", "")
    ]
    return " ".join(fields).lower()

# =========================
# BUILD BM25
# =========================

for category, file_name in FILES.items():
    with open(METADATA_DIR / file_name, "r") as f:
        data = json.load(f)

    corpus = []
    id_map = []

    for item in data:
        text = metadata_to_text(item)
        tokens = word_tokenize(text)
        corpus.append(tokens)
        id_map.append(item)

    bm25 = BM25Okapi(corpus)

    with open(OUTPUT_DIR / f"{category}_bm25.pkl", "wb") as f:
        pickle.dump(
            {
                "bm25": bm25,
                "corpus": corpus,
                "id_map": id_map
            },
            f
        )

    print(f"BM25 index built for {category} ({len(corpus)} documents)")
