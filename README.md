<div align="center">

# DocuRAG — Enterprise RAG Engine with Local LLMs

A fully local, privacy-preserving Retrieval-Augmented Generation (RAG) system for querying enterprise PDF documents using quantized open-source LLMs — no external API calls, no data leaving your infrastructure.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-1C3C3C.svg)](https://www.langchain.com/)
[![llama.cpp](https://img.shields.io/badge/Inference-llama.cpp-000000.svg)](https://github.com/ggerganov/llama.cpp)
[![FAISS](https://img.shields.io/badge/Vector%20Store-FAISS-005571.svg)](https://github.com/facebookresearch/faiss)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Supported Models](#supported-models)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)

## Overview

DocuRAG is a Retrieval-Augmented Generation pipeline built to run entirely on local infrastructure. It ingests enterprise PDF documents — including both free text and tabular data — chunks and embeds them, and serves natural language answers using quantized GGUF language models run through `llama.cpp`. Because inference, embeddings, and vector search all run locally, no document content or query ever leaves the host machine, making it suitable for confidential or regulated enterprise data.

## Key Features

- **Local-Only Inference** — Runs quantized GGUF models via `llama-cpp-python`; no external LLM API required
- **Selectable Model Backend** — Swap between multiple pre-configured Mistral, Mixtral, and lightweight models at runtime via an interactive CLI menu
- **Dual-Layer Chunking (Parent/Child Retrieval)** — Uses LangChain's `ParentDocumentRetriever` to embed small, precise child chunks for retrieval while returning larger parent chunks for richer context
- **Table-Aware PDF Extraction** — Extracts both narrative text (via PyMuPDF) and structured tables (via `img2table` + BeautifulSoup) from source PDFs, preserving table structure as JSON
- **Local Embeddings** — Uses a locally-hosted `all-MiniLM-L6-v2` sentence-transformer model for vector embeddings, avoiding external embedding API calls
- **FAISS Vector Store** — Efficient similarity search over embedded document chunks
- **CLI and Web Interfaces** — Query documents through either a command-line interface (`rag_cli.py`) or a web UI (`app.py`)
- **Selective Document Ingestion** — Choose which documents in `docs/` to index via `select_docs.py`

## Architecture

The system follows a two-stage retrieval architecture rather than naive single-chunk RAG:

1. **Document Extraction**
   `extract_docs_from_pdf.py` processes each source PDF twice: once to pull plain text page-by-page using PyMuPDF (`fitz`), and once to detect and extract tables using `img2table`, converting each table into structured JSON via BeautifulSoup-based HTML parsing.

2. **Parent/Child Splitting**
   Extracted text is wrapped into LangChain `Document` objects ("parent" documents). A `RecursiveCharacterTextSplitter` then derives smaller "child" chunks (500 chars, 30 overlap) from each parent (2000 chars, 1000 overlap), with each child chunk tagged with its parent's ID in metadata.

3. **Embedding and Indexing**
   Parent documents are embedded using a local `HuggingFaceEmbeddings` model and indexed in a FAISS vector store. Parent documents are also cached in an `InMemoryStore` docstore, keyed by parent ID.

4. **Retrieval**
   A `ParentDocumentRetriever` performs similarity search over the child-chunk embedding space, then resolves matches back to their full parent document — balancing retrieval precision (small chunks) with generation context quality (larger, coherent chunks).

5. **Answer Generation**
   The retrieved parent context and user query are passed to a locally-running GGUF model via `llama-cpp-python`, which streams back a generated answer.

## Supported Models

Model selection is configurable via `models.py`, which maintains an indexed registry of local GGUF checkpoints. At runtime, `select_model()` either accepts a model index directly or presents an interactive menu:

| Family        | Example Variants                                                    |
|---------------|------------------------------------------------------------------------|
| Mistral 7B    | Instruct v0.2 (Q6_K), Instruct v0.3 (Q4_1, Q8_0, F16), Code 16K QLoRA (Q8_0) |
| Mistral Nemo  | Instruct 2407 (Q4_K_M)                                                |
| Mistral Small | 24B Instruct 2501 (BF16, Q8_0, Q4_K_M)                                |
| Mixtral 8x7B  | Instruct v0.1 (Q8_0), Base v0.1 (Q4_K_M)                              |
| Lightweight   | Phi-2 (Q4_K_M), TinyLlama 1.1B Chat (Q5_K_M)                          |

Models are swapped without code changes by editing the model index passed to `select_model()`, making it straightforward to trade off inference speed against answer quality depending on available hardware.

## Tech Stack

| Layer                | Technology                                              |
|----------------------|------------------------------------------------------------|
| LLM Inference        | `llama-cpp-python` (GGUF quantized models)               |
| Orchestration        | LangChain (`langchain-community`, `langchain-text-splitters`) |
| Retrieval            | `ParentDocumentRetriever`, `InMemoryStore`                |
| Vector Store         | FAISS                                                     |
| Embeddings           | HuggingFace `sentence-transformers` (`all-MiniLM-L6-v2`) |
| PDF Text Extraction  | PyMuPDF (`fitz`)                                          |
| PDF Table Extraction | `img2table`, BeautifulSoup                                |
| Backend              | Python, Flask                                             |
| Frontend             | HTML templates, static assets                             |

## Prerequisites

- Python 3.8 or higher
- `pip` for package management
- Local GGUF model file(s) downloaded and placed under `/models/` (paths configured in `models.py`)
- A local copy of the `all-MiniLM-L6-v2` embedding model under `/models/all-MiniLM-L6-v2`
- Sufficient RAM/VRAM for your chosen quantized model (lightweight options like TinyLlama or Phi-2 are recommended for constrained hardware)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/adhvaith267/rag-model.git
cd rag-model
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your documents

Place the source PDF files into `rawdocs/`, and use `select_docs.py` to choose which ones get processed into `docs/` for indexing.

### 5. Configure model paths

Update the `path` values in `models.py` to point to your local GGUF model files, and set the embedding model path in `rag.py` if it differs from `/models/all-MiniLM-L6-v2`.

## Configuration

| File                     | Purpose                                                        |
|--------------------------|---------------------------------------------------------------|
| `models.py`              | Registry of available GGUF models and interactive selector    |
| `select_docs.py`         | Chooses which documents from `rawdocs/` are indexed           |
| `extract_docs_from_pdf.py` | Text and table extraction logic for source PDFs              |
| `rag.py`                 | Core RAG pipeline: chunking, embedding, indexing, retrieval    |
| `rag_cli.py`             | Command-line interface for querying the RAG pipeline          |
| `app.py`                 | Web application entry point                                   |

## Usage

### Command-line interface

```bash
python rag_cli.py
```

Select a model from the interactive menu (or hardcode an index via `select_model(index)`), then ask questions about the indexed documents directly from the terminal.

### Web interface

```bash
python app.py
```

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

Use the input box to ask natural language questions; answers are generated using retrieved document context and the selected local LLM.

## Project Structure

```
rag-model/
├── docs/                       # Processed/selected documents ready for indexing
├── rawdocs/                    # Raw source PDF documents
├── static/
│   └── images/                 # Static assets for the web UI
├── templates/                  # Web UI HTML templates
├── .gitignore
├── app.py                      # Flask web application entry point
├── extract_docs_from_pdf.py    # PDF text and table extraction
├── models.py                   # GGUF model registry and selector
├── rag.py                      # Core RAG pipeline (chunking, embedding, retrieval, generation)
├── rag_cli.py                  # CLI for querying the RAG pipeline
├── select_docs.py              # Document selection utility
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```



<div align="center">
Built with LangChain, llama.cpp, and FAISS
</div>
