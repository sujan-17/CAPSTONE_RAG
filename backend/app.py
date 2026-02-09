from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image
import io
import numpy as np
import json

from query_router import route_query
from query_rewriter import rewrite_query
from ocr_pipeline import ocr_pipeline
from hybrid_search import hybrid_search
from reranker import rerank

# =========================
# APP SETUP
# =========================

app = FastAPI(title="Jewellery Multimodal RAG")

app.mount(
    "/static",
    StaticFiles(directory="data/raw"),
    name="static"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# HEALTH CHECK
# =========================

@app.get("/")
def health():
    return {"status": "ok"}

# =========================
# TEXT QUERY ENDPOINT
# =========================

@app.post("/search/text")
def search_text(query: str):
    rewritten_query = rewrite_query(query)

    routed = route_query(rewritten_query)
    category = routed["category"]

    candidates = hybrid_search(
        query=rewritten_query,
        category=category,
        top_k=15
    )

    final_results = rerank(
        query=rewritten_query,
        candidates=candidates,
        top_k=10
    )

    return {
        "original_query": query,
        "rewritten_query": rewritten_query,
        "category": category,
        "results": final_results
    }

# =========================
# IMAGE QUERY ENDPOINT (FIXED)
# =========================

@app.post("/search/image")
async def search_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    result = ocr_pipeline(image)

    # ---- HANDWRITTEN IMAGE ----
    if result["type"] == "handwritten":
        rewritten_text = rewrite_query(result["text"])

        routed = route_query(rewritten_text)
        category = routed["category"]

        candidates = hybrid_search(
            query=rewritten_text,
            category=category,
            top_k=15
        )

        final_results = rerank(
            query=rewritten_text,
            candidates=candidates,
            top_k=10
        )

        return {
            "query_type": "handwritten",
            "original_text": result["text"],
            "rewritten_query": rewritten_text,
            "category": category,
            "results": final_results
        }

    # ---- JEWEL / SKETCH IMAGE (CRITICAL FIX) ----
    image_description = result["description"]
    rewritten_query = rewrite_query(image_description)

    routed = route_query(rewritten_query)
    category = routed["category"]

    candidates = hybrid_search(
        query=rewritten_query,
        category=category,
        top_k=15
    )

    final_results = rerank(
        query=rewritten_query,
        candidates=candidates,
        top_k=10
    )

    return {
        "query_type": "image",
        "image_description": image_description,
        "rewritten_query": rewritten_query,
        "category": category,
        "results": final_results
    }
