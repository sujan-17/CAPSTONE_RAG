"""
Category-aware FAISS retrieval
Ring → ring only
Necklace → necklace only
Both → no filter
"""

import json
from pathlib import Path

import faiss
import numpy as np
import torch
from transformers import CLIPProcessor, CLIPModel

# =========================
# CONFIG
# =========================

FAISS_INDEX_PATH = Path("faiss/image.index")
ID_MAPPING_PATH = Path("embeddings/id_mapping.json")

MODEL_NAME = "openai/clip-vit-large-patch14"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

TOP_K = 10
OVERFETCH_K = 50  # fetch more, then filter

# =========================
# LOAD EVERYTHING
# =========================

index = faiss.read_index(str(FAISS_INDEX_PATH))

with open(ID_MAPPING_PATH, "r") as f:
    id_mapping = json.load(f)

model = CLIPModel.from_pretrained(MODEL_NAME).to(DEVICE)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)

model.eval()

# =========================
# QUERY ENCODERS
# =========================

def encode_text(query: str) -> np.ndarray:
    inputs = processor(text=query, return_tensors="pt", padding=True).to(DEVICE)

    with torch.no_grad():
        outputs = model.text_model(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"]
        )

        text_features = outputs.pooler_output
        text_features = model.text_projection(text_features)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)

    return text_features.cpu().numpy().astype("float32").reshape(1,-1)

def encode_image(image):
    inputs = processor(images=image, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        outputs = model.vision_model(**inputs)
        image_features = outputs.pooler_output
        image_features = model.visual_projection(image_features)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)

    return image_features.cpu().numpy().astype("float32").reshape(1,-1)


# =========================
# CATEGORY-AWARE SEARCH
# =========================

def faiss_search(query_embedding, category="both", top_k=TOP_K):
    scores, indices = index.search(query_embedding, OVERFETCH_K)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        meta = id_mapping[idx]

        if category != "both" and meta["category"] != category:
            continue

        results.append({
            "score": float(score),
            "faiss_index": int(idx),
            "id": meta["id"],
            "category": meta["category"],
            "image_name": meta["image_name"],
            "metadata": meta["metadata"]
        })

        if len(results) >= top_k:
            break

    return results
