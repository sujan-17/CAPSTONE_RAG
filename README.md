# Jewellery Multimodal RAG

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Vite%20Frontend-61dafb)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-orange)
![CLIP](https://img.shields.io/badge/CLIP-Multimodal-purple)

AI-powered multimodal jewellery retrieval system with a FastAPI backend and a React/Vite frontend. The app supports text search, image search, handwritten query understanding, hybrid retrieval, and reranking for more relevant jewellery results.

## Overview

This project is a full-stack multimodal retrieval application for jewellery discovery.

Main capabilities:

- Text search with LLM-based query rewriting
- Category routing for `ring`, `necklace`, or `both`
- Hybrid retrieval using FAISS dense search and BM25 lexical search
- Cross-encoder reranking for final result quality
- Image search using CLIP image embeddings
- Handwritten text handling through the OCR + LLM pipeline
- Modern React frontend with filters, result cards, and modal details

Current dataset:

- 189 rings
- 301 necklaces
- 490 total jewellery items

## Architecture

### Text Query Pipeline

1. User enters a jewellery query.
2. The query is rewritten by the LLM query rewriter.
3. The query router predicts the category: `ring`, `necklace`, or `both`.
4. Hybrid retrieval runs:
   - FAISS dense retrieval with CLIP text embeddings
   - BM25 lexical retrieval
5. Retrieved candidates are reranked with a cross-encoder.
6. The frontend displays the final ranked results.

### Image Query Pipeline

1. User uploads an image.
2. The OCR pipeline checks whether the image contains handwritten text.
3. If handwritten text is detected:
   - Text is extracted
   - The app falls back to the text-query pipeline
4. Otherwise:
   - The image is encoded with CLIP
   - FAISS returns visually similar jewellery items

## Tech Stack

### Backend

- FastAPI
- Uvicorn
- FAISS
- Transformers
- SentenceTransformers
- OpenAI-compatible LLM API
- Pillow
- NumPy
- rank-bm25
- Torch
- OpenCV

### Frontend

- React
- Vite
- Axios
- Custom CSS

## Project Structure

```text
CAPSTONE_RAG/
|-- backend/
|   |-- __init__.py
|   |-- app.py
|   |-- query_rewriter.py
|   |-- query_router.py
|   |-- ocr_pipeline.py
|   |-- hybrid_search.py
|   |-- bm25_search.py
|   |-- faiss_search.py
|   |-- reranker.py
|   |-- create_embeddings.py
|   |-- create_faiss_index.py
|   |-- build_bm25.py
|   |-- data/
|   |-- embeddings/
|   |-- faiss/
|   `-- bm25/
|-- frontend/
|   |-- index.html
|   |-- package.json
|   |-- vite.config.js
|   `-- src/
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## Setup

### 1. Clone the Repository

```powershell
git clone <your-repo-url>
cd CAPSTONE_RAG
```

### 2. Create and Activate a Python Virtual Environment

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies

```powershell
cd frontend
npm install
cd ..
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://your-provider-base-url
LLM_MODEL=your_model_name
```

Used by:

- `backend/query_rewriter.py`
- `backend/ocr_pipeline.py`

## Run the Project

Start the backend from the project root:

```powershell
python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

Backend URL:

```text
http://localhost:8000
```

In a second terminal, start the frontend:

```powershell
cd frontend
npm run dev
```

Frontend URL:

```text
http://localhost:3000
```

## API Endpoints

### Health Check

```text
GET /
```

### Text Search

```text
POST /search/text?query=<query>
```

Pipeline includes:

- Query rewriting
- Category routing
- Hybrid retrieval
- Reranking

### Image Search

```text
POST /search/image
```

Accepts image uploads and performs:

- Handwritten text detection
- OCR-based text fallback
- CLIP image retrieval

### Static Images

```text
GET /static/<category>/<image_name>
```

Serves jewellery images from the backend dataset folders.

## Included Retrieval Artifacts

Prebuilt retrieval artifacts already included:

```text
backend/bm25/ring_bm25.pkl
backend/bm25/necklace_bm25.pkl
backend/embeddings/image_embeddings.npy
backend/embeddings/id_mapping.json
backend/faiss/image.index
```

## Rebuilding Indexes

Only needed if the dataset changes.

### Build BM25

```powershell
python backend/build_bm25.py
```

### Generate CLIP Embeddings

```powershell
python backend/create_embeddings.py
```

### Build FAISS Index

```powershell
python backend/create_faiss_index.py
```

## Metadata Fields

Jewellery metadata used for retrieval and filtering:

- `category`
- `material`
- `stone_type`
- `stone_shape`
- `color`
- `short_description`
- `image_name`

Supported categories:

- `ring`
- `necklace`

## Frontend Features

- Text query search
- Image upload search
- Result grid layout
- Metadata filter sidebar
- Result detail modal
- Processed query display
- Query type and category indicators

## Example Queries

```text
gold ring with diamond
emerald necklace
plain wedding band
gold ring with red stone
```

You can also:

- Upload a jewellery photo
- Upload a handwritten jewellery request
- Upload a Jewel Sketch
