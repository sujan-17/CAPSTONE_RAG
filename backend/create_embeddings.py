"""
Create CLIP image embeddings for jewellery dataset
using ViT-L/14
"""

import json
import os
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from tqdm import tqdm
from transformers import CLIPProcessor, CLIPModel

# =========================
# CONFIG
# =========================

PROCESSED_DIR = Path("data/processed")
METADATA_DIR = Path("data/metadata")
OUTPUT_DIR = Path("embeddings")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "openai/clip-vit-large-patch14"

# =========================
# SETUP
# =========================

OUTPUT_DIR.mkdir(exist_ok=True)

model = CLIPModel.from_pretrained(MODEL_NAME).to(DEVICE)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)

model.eval()

# =========================
# LOAD METADATA
# =========================

def load_metadata():
    all_items = []

    for file in ["ring_metadata.json", "necklace_metadata.json"]:
        path = METADATA_DIR / file
        with open(path, "r") as f:
            data = json.load(f)
            all_items.extend(data)

    return all_items

metadata_items = load_metadata()

# =========================
# IMAGE EMBEDDING LOOP
# =========================

embeddings = []
id_mapping = []

idx = 0

with torch.no_grad():
    for item in tqdm(metadata_items, desc="Creating embeddings"):
        category = item["category"]
        image_name = item["image_name"]

        image_path = PROCESSED_DIR / category / image_name

        if not image_path.exists():
            continue

        image = Image.open(image_path).convert("RGB")

        inputs = processor(
            images=image,
            return_tensors="pt"
        ).to(DEVICE)

        outputs = model.vision_model(**inputs)
        image_features = outputs.pooler_output
        image_features = model.visual_projection(image_features)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)


        embeddings.append(image_features.cpu().numpy()[0])

        id_mapping.append({
            "faiss_index": idx,
            "id": item["id"],
            "category": category,
            "image_name": image_name,
            "metadata": item
        })

        idx += 1

# =========================
# SAVE OUTPUTS
# =========================

embeddings = np.vstack(embeddings).astype("float32")

np.save(OUTPUT_DIR / "image_embeddings.npy", embeddings)

with open(OUTPUT_DIR / "id_mapping.json", "w") as f:
    json.dump(id_mapping, f, indent=2)

print(f"Saved {len(embeddings)} embeddings")


