# 💍 Jewellery Multimodal RAG

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-orange)
![CLIP](https://img.shields.io/badge/CLIP-Multimodal-purple)


AI-powered **multimodal jewellery retrieval system** supporting **text search, image search, OCR-based handwritten queries, and hybrid retrieval** with a modern React interface.

---

# 📖 Overview

This project implements a **full-stack multimodal RAG-style retrieval system** for jewellery discovery.

The system combines:

* **Text Search** with LLM query rewriting
* **Image Search** using CLIP embeddings
* **Handwritten Query Understanding** using OCR + LLM
* **Hybrid Retrieval** (FAISS dense search + BM25 lexical search)
* **Cross-Encoder Reranking** for improved relevance
* **Interactive React UI** for browsing jewellery results

Current dataset:

* **189 rings**
* **301 necklaces**
* **490 total jewellery items**

---

# ⚙️ System Architecture

## Text Query Pipeline

1. User enters a jewellery query
2. Query is rewritten using an LLM
3. Router predicts category (`ring`, `necklace`, `both`)
4. Hybrid retrieval runs:

   * **CLIP embedding search (FAISS)**
   * **BM25 lexical retrieval**
5. Results are reranked using a **cross-encoder**
6. Frontend displays the best matching jewellery items

---

## Image Query Pipeline

1. User uploads an image
2. OCR pipeline checks if it contains **handwritten text**
3. If handwritten text is detected:

   * Text is extracted
   * System switches to the **text query pipeline**
4. Otherwise:

   * Image is encoded using **CLIP**
   * FAISS retrieves visually similar jewellery items

---

# 🧠 Tech Stack

## Backend

* FastAPI
* FAISS
* Transformers
* SentenceTransformers
* NLTK
* Pillow
* NumPy
* OpenAI-compatible LLM API

## Frontend

* React 18
* Vite
* Axios

---

# 📂 Project Structure

```
CAPSTONE_RAG/
│
├── backend/
│   ├── app.py
│   ├── query_rewriter.py
│   ├── query_router.py
│   ├── ocr_pipeline.py
│   ├── hybrid_search.py
│   ├── bm25_search.py
│   ├── faiss_search.py
│   ├── reranker.py
│   ├── create_embeddings.py
│   ├── create_faiss_index.py
│   ├── build_bm25.py
│   │
│   ├── data/
│   │   ├── metadata/
│   │   ├── raw/
│   │   └── processed/
│   │
│   ├── embeddings/
│   ├── faiss/
│   └── bm25/
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── components/
│
├── requirements.txt
└── README.md
```

---

# 🚀 Quick Start

## 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd CAPSTONE_RAG
```

---

## 2️⃣ Backend Setup

```bash
cd backend

python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r ../requirements.txt
```

Download NLTK tokenizer:

```bash
python -c "import nltk; nltk.download('punkt')"
```

---

## 3️⃣ Environment Variables

Create a `.env` file in the project root:

```
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://your-provider-base-url
LLM_MODEL=your_model_name
```

Used by:

* `query_rewriter.py`
* `ocr_pipeline.py`

---

## 4️⃣ Start Backend

From the `backend` folder:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Backend URL:

```
http://localhost:8000
```

---

## 5️⃣ Start Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```
http://localhost:3000
```

---

# 🔍 API Endpoints

### Health Check

```
GET /
```

---

### Text Search

```
POST /search/text?query=<query>
```

Pipeline includes:

* Query rewriting
* Category routing
* Hybrid retrieval
* Reranking

---

### Image Search

```
POST /search/image
```

Accepts image uploads and performs:

* Handwritten text detection
* OCR extraction
* CLIP image retrieval

---

# 📦 Included Retrieval Artifacts

Prebuilt indexes allow the system to run immediately:

```
backend/bm25/ring_bm25.pkl
backend/bm25/necklace_bm25.pkl
backend/embeddings/image_embeddings.npy
backend/embeddings/id_mapping.json
backend/faiss/image.index
```

---

# 🔄 Rebuilding Indexes

Only required if the dataset changes.

### Build BM25

```bash
python build_bm25.py
```

### Generate CLIP Embeddings

```bash
python create_embeddings.py
```

### Build FAISS Index

```bash
python create_faiss_index.py
```

---

# 💎 Metadata Fields

Jewellery metadata used for retrieval and filtering:

* `category`
* `material`
* `stone_type`
* `stone_shape`
* `color`
* `short_description`
* `image_name`

Supported categories:

* **ring**
* **necklace**

---

# 🖥 Frontend Features

* Text search
* Image upload search
* Jewellery result grid
* Metadata filters
* Result detail modal
* Processed query display
* Category and query badges

---

# 🎯 Demo Examples

Example queries:

```
gold ring with diamond
emerald necklace
plain wedding band
```

You can also:

* Upload a **jewellery photo**
* Upload a **handwritten jewellery requirement**

---

# 🧩 Demo Goal

This project demonstrates a **compact multimodal RAG pipeline** where:

* Text queries are rewritten and routed
* Images are embedded using CLIP
* Sparse + dense retrieval are fused
* Cross-encoder reranking improves relevance
* A modern frontend enables interactive search

---
