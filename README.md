# 💎 Jewellery Multimodal RAG System

A high-accuracy **Multimodal Retrieval-Augmented Generation (RAG)** system for jewellery search that supports **text queries, image queries, sketches, and handwritten inputs** using modern vision-language models.

This project focuses on **Similarity-Based Retrieval** for a small, curated jewellery dataset.

---

## 📌 Key Features

- 🔍 Text-based jewellery search
- 🖼️ Image-based search (jewel images & sketches)
- ✍️ Handwritten query understanding
- 🧠 LLM-based query rewriting and image understanding
- 🧩 Category-aware routing (ring / necklace)
- 🔗 Multimodal embeddings using CLIP
- ⚡ Hybrid retrieval (Dense + Sparse)
- 🎯 Cross-encoder reranking for final accuracy
- 🖥️ Interactive UI using Streamlit

---

## 🧠 System Architecture (High Level)

User Input (Text / Image)
↓
Query Rewriter / Image Description (LLM)
↓
Query Router (Ring / Necklace / Both)
↓
Hybrid Retrieval
├─ Dense Search (CLIP + FAISS)
└─ Sparse Search (BM25 on metadata)
↓
Score Fusion & Normalization
↓
Cross-Encoder Reranker
↓
Final Ranked Results


---

## 🗂️ Dataset Overview

- Total images: ~500
- Categories:
  - Rings
  - Necklaces
- Each image has structured metadata:
  - Category
  - Material
  - Stone type
  - Stone shape
  - Color
  - Short description

Metadata is stored separately for rings and necklaces.

---

## 🧪 Models & Techniques Used

### 🔹 Multimodal Embeddings
- **Model:** CLIP ViT-Large Patch-14
- **Embedding dimension:** 768
- **Normalization:** L2-normalized
- **Similarity:** Cosine similarity via FAISS Inner Product

### 🔹 Dense Retrieval
- FAISS `IndexFlatIP`
- Exact cosine similarity search
- Optimized for small datasets

### 🔹 Sparse Retrieval
- BM25 over metadata text
- Captures keyword-level relevance

### 🔹 Hybrid Search
- Weighted fusion of FAISS and BM25 scores
- Min-max score normalization

### 🔹 Reranking
- Cross-encoder (sentence-transformers)
- Joint query-metadata relevance scoring
- Final accuracy refinement step

### 🔹 Query Rewriting
- LLM-based rewriting
- Removes ambiguity and negative constraints
- Produces retrieval-optimized queries

### 🔹 Image & Handwriting Understanding
- Vision-capable LLM
- Converts images into semantic descriptions
- Avoids limitations of traditional OCR

---

## 🖥️ Tech Stack

**Backend**
- Python
- FastAPI
- FAISS
- Sentence-Transformers
- HuggingFace Transformers

**Frontend**
- Streamlit

**Models**
- CLIP (Vision-Language)
- Cross-Encoder (Reranker)
- Vision-LLM (Image understanding & rewriting)

---
