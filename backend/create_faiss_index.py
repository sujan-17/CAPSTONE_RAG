"""
Build FAISS index for CLIP image embeddings
Cosine similarity (L2-normalized vectors)
"""

import faiss
import numpy as np
from pathlib import Path

# =========================
# CONFIG
# =========================

EMBEDDING_PATH = Path("embeddings/image_embeddings.npy")
FAISS_DIR = Path("faiss")
INDEX_PATH = FAISS_DIR / "image.index"

FAISS_DIR.mkdir(exist_ok=True)

# =========================
# LOAD EMBEDDINGS
# =========================

embeddings = np.load(EMBEDDING_PATH).astype("float32")
dim = embeddings.shape[1]

# =========================
# BUILD INDEX (ACCURACY FIRST)
# =========================

index = faiss.IndexFlatIP(dim)  # inner product = cosine (since normalized)
index.add(embeddings)

faiss.write_index(index, str(INDEX_PATH))

print(f"FAISS index built with {index.ntotal} vectors")
