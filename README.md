<div align="center">

# LLM - A RAG Model for Enterprise Data

A Retrieval-Augmented Generation (RAG) system that answers natural language questions using your own enterprise documents.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-black.svg)](https://flask.palletsprojects.com/)
[![FAISS](https://img.shields.io/badge/Vector%20Store-FAISS-005571.svg)](https://github.com/facebookresearch/faiss)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline designed to work with enterprise data. It allows users to ask questions in natural language and receive answers grounded in a given set of documents. The system uses a large language model (LLM) to understand user queries and retrieve relevant information from a vectorized knowledge base.

## Features

- **Document Processing** — Extracts text from PDF documents and stores it in a searchable vector database
- **Natural Language Queries** — Ask questions in plain English
- **Contextual Answers** — Answers are generated using the actual content of the provided documents
- **Web Interface** — A simple UI for interacting with the model

## How It Works

The application follows a standard RAG architecture:

1. **Data Ingestion** — PDF documents placed in the `docs/` directory are processed. Text is extracted, split into chunks, and converted into vector embeddings.
2. **Vector Store** — These embeddings are stored in a FAISS vector database, enabling efficient similarity search.
3. **User Query** — When a user asks a question, the query is converted into a vector embedding.
4. **Information Retrieval** — The system searches the vector store for document chunks most relevant to the query.
5. **Answer Generation** — The retrieved context and the original question are passed to an LLM, which generates a coherent, grounded answer.

## Tech Stack

| Layer          | Technology              |
|----------------|---------------------------|
| Backend        | Python, Flask            |
| LLM / Embeddings | Large Language Model (LLM) |
| Vector Store   | FAISS                    |
| Document Parsing | PDF text extraction     |
| Frontend       | HTML / Web UI            |

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

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

Place the PDF files you want to query into the `docs/` directory.

## Usage

### 1. Start the application

```bash
python app.py
```

### 2. Access the web interface

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

### 3. Ask questions

Use the input box to ask questions about the documents you provided. The model will retrieve relevant context and generate an answer based on your documents.

## Project Structure

```
rag-model/
├── docs/                 # Source PDF documents to be indexed
├── templates/            # Web UI templates
├── app.py                # Application entry point
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

> Note: Update this section if your actual folder layout differs (e.g. separate modules for ingestion, embeddings, or the vector store).

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">
Built with Flask, FAISS, and LLMs
</div>
