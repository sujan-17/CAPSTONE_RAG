# Jewellery Multimodal RAG

> AI-powered jewellery retrieval system with text search, image search, query rewriting, OCR-assisted understanding, hybrid retrieval, and a React UI.

## Overview

This project is a full-stack multimodal retrieval application for jewellery discovery. It combines:

- `Text search` with query rewriting and category routing
- `Image search` using CLIP embeddings + FAISS similarity search
- `Handwritten query support` through an LLM-based OCR pipeline
- `Hybrid retrieval` using dense search (FAISS) + sparse search (BM25)
- `Reranking` with a cross-encoder for better final relevance
- `Interactive frontend` with filters, previews, and result modals

The current dataset contains:

- `189` ring items
- `301` necklace items
- `490` total jewellery records

## What The App Does

### Text query flow

1. User enters a jewellery query
2. The backend rewrites the query using an LLM
3. A router predicts whether the query targets `ring`, `necklace`, or `both`
4. Hybrid retrieval combines:
   - CLIP text embedding search through `FAISS`
   - lexical search through `BM25`
5. A cross-encoder reranks the retrieved candidates
6. The frontend shows filtered, image-based results

### Image query flow

1. User uploads an image
2. The OCR pipeline checks whether the image contains handwritten text
3. If handwritten text is detected:
   - text is extracted
   - the system switches into the text-query pipeline
4. If it is a jewellery image or sketch:
   - the image is encoded with `CLIP`
   - results are retrieved directly from `FAISS`

## Stack

### Backend

- `FastAPI`
- `FAISS`
- `Transformers`
- `SentenceTransformers`
- `OpenAI-compatible API client`
- `NLTK`
- `Pillow`
- `NumPy`

### Frontend

- `React 18`
- `Vite`
- `Axios`

## Project Structure

```text
CAPSTONE_RAG/
|- backend/
|  |- app.py                  # FastAPI server
|  |- query_rewriter.py       # LLM-based query rewriting
|  |- query_router.py         # ring / necklace / both router
|  |- ocr_pipeline.py         # handwritten text detection + extraction
|  |- hybrid_search.py        # FAISS + BM25 fusion
|  |- bm25_search.py          # sparse retrieval
|  |- faiss_search.py         # dense retrieval with CLIP
|  |- reranker.py             # cross-encoder reranking
|  |- create_embeddings.py    # build image embeddings
|  |- create_faiss_index.py   # build FAISS index
|  |- build_bm25.py           # build BM25 indexes
|  |- data/
|  |  |- metadata/            # jewellery metadata JSON
|  |  |- raw/                 # raw images served by FastAPI
|  |  |- processed/           # processed images for embeddings
|  |- embeddings/             # saved CLIP embeddings + id mapping
|  |- faiss/                  # FAISS index
|  |- bm25/                   # BM25 index files
|- frontend/
|  |- src/
|  |  |- App.jsx              # main UI
|  |  |- components/          # search, filters, cards, modal
|  |- package.json
|- .env
|- README.md
```

## Current Backend Endpoints

### `GET /`

Health check endpoint.

### `POST /search/text?query=...`

Runs:

- query rewriting
- category routing
- hybrid retrieval
- reranking

### `POST /search/image`

Accepts multipart image upload:

- handwritten image -> OCR + text pipeline
- jewellery image -> CLIP + FAISS image retrieval

## Quick Start

### 1. Clone and open the project

```powershell
git clone <your-repo-url>
cd CAPSTONE_RAG
```

### 2. Backend setup

Create and activate a Python virtual environment:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
```

Install the backend dependencies:

```powershell
pip install fastapi uvicorn python-multipart pillow numpy nltk rank-bm25 faiss-cpu torch transformers sentence-transformers openai python-dotenv opencv-python tqdm
```

Download the tokenizer data required by NLTK:

```powershell
python -c "import nltk; nltk.download('punkt')"
```

### 3. Environment variables

Create a root `.env` file with your OpenAI-compatible endpoint details:

```env
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://your-provider-base-url
LLM_MODEL=your_model_name
```

Used by:

- `backend/query_rewriter.py`
- `backend/ocr_pipeline.py`

### 4. Start the backend

Run the API from the `backend` directory:

```powershell
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Backend URL:

```text
http://localhost:8000
```

### 5. Frontend setup

Open a new terminal:

```powershell
cd frontend
npm install
```

Start the React app:

```powershell
npm run dev
```

Frontend URL:

```text
http://localhost:3000
```

## Ready-To-Use Assets Included

This repository already contains prebuilt retrieval artifacts:

- `backend/bm25/ring_bm25.pkl`
- `backend/bm25/necklace_bm25.pkl`
- `backend/embeddings/image_embeddings.npy`
- `backend/embeddings/id_mapping.json`
- `backend/faiss/image.index`

That means the project can be run directly without rebuilding indexes first, as long as dependencies and environment variables are configured correctly.

## Rebuilding Indexes

Use these only if you modify metadata, processed images, or the retrieval corpus.

### Rebuild BM25

```powershell
cd backend
python build_bm25.py
```

### Rebuild CLIP embeddings

```powershell
cd backend
python create_embeddings.py
```

### Rebuild FAISS index

```powershell
cd backend
python create_faiss_index.py
```

## Search Categories And Metadata

The system currently works with two jewellery classes:

- `ring`
- `necklace`

Metadata fields used across retrieval and filtering include:

- `category`
- `material`
- `stone_type`
- `stone_shape`
- `color`
- `short_description`
- `image_name`

## Frontend Features

- Text search bar
- Image upload search
- Result grid with jewellery cards
- Filter sidebar for metadata-driven refinement
- Result detail modal
- Processed query display
- Query type and category badges

## Notes Before Running

- Run the backend from inside the `backend` folder, because paths like `data/raw`, `bm25`, `faiss`, and `embeddings` are relative to that directory.
- The frontend currently talks to `http://localhost:8000` directly.
- On first model load, `transformers` and `sentence-transformers` may download model weights if they are not already cached.
- `faiss-cpu` is fine for local development; if you use GPU FAISS, update the install accordingly.
- The included `.env` file should not contain production secrets in a public repository.

## Suggested Run Order

```text
1. Start backend on port 8000
2. Start frontend on port 3000
3. Open the browser
4. Search by text or upload an image
```

## Example Queries

- `gold ring with diamond`
- `emerald necklace`
- `plain wedding band`
- upload a jewellery photo
- upload a handwritten jewellery requirement

## Known Gaps

- There is no pinned `requirements.txt` yet; dependency installation is currently command-based.
- The frontend has a few visible text encoding artifacts in UI strings.
- The Vite proxy is configured, but the frontend code currently calls the backend directly via `http://localhost:8000`.

## Demo Goal

This repository is well suited for demonstrating a compact multimodal RAG pipeline where:

- text is normalized and routed
- images are embedded and retrieved semantically
- sparse and dense retrieval are fused
- a reranker improves final output quality
- a clean frontend makes the system easy to test interactively
