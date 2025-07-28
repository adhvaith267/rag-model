# LLM - A RAG Model for Enterprise Data

This project implements a Retrieval-Augmented Generation (RAG) model designed to work with enterprise data. It allows users to ask questions in natural language and receive answers based on a given set of documents. The system uses a large language model (LLM) to understand and process user queries and retrieve relevant information from a vectorized knowledge base.

## Features

-   **Document Processing**: Extracts text from PDF documents and stores them in a searchable vector database.
-   **Natural Language Queries**: Users can ask questions in plain English.
-   **Contextual Answers**: The model uses the content of the provided documents to generate answers.
-   **Web Interface**: A simple web UI for interacting with the model.

## How it Works

The application follows a standard RAG architecture:

1.  **Data Ingestion**: PDF documents placed in the `docs/` directory are processed. The text is extracted, split into chunks, and converted into vector embeddings.
2.  **Vector Store**: These embeddings are stored in a FAISS vector database, which allows for efficient similarity searches.
3.  **User Query**: When a user asks a question, the query is also converted into a vector embedding.
4.  **Information Retrieval**: The system searches the vector store for document chunks that are most relevant to the user's query.
5.  **Answer Generation**: The retrieved text chunks (context) and the original user question are passed to a large language model, which then generates a coherent answer.

## Project Structure

```
/
|-- app.py                  # Main Flask application
|-- rag.py                  # Core RAG logic
|-- models.py               # Model definitions (e.g., embeddings)
|-- extract_docs_from_pdf.py # Script to process PDFs
|-- select_docs.py          # Script to select documents for processing
|-- requirements.txt        # Python dependencies
|-- .gitignore              # Files and directories to be ignored by Git
|-- docs/                   # Directory for processed documents (add your PDFs here)
|-- rawdocs/                # Directory for raw documents
|-- templates/
|   |-- index.html          # Web interface
|-- static/
    |-- ...
```

## Setup and Installation

### Prerequisites

-   Python 3.8+
-   `pip` for package management

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Add your documents:**
    Place the PDF files you want to query into the `docs/` directory.

## How to Run

1.  **Start the application:**
    ```bash
    python app.py
    ```

2.  **Access the web interface:**
    Open your web browser and navigate to `http://127.0.0.1:5000`.

3.  **Ask questions:**
    Use the input box to ask questions about the documents you provided.

## Privacy

To protect privacy, the `docs/` and `rawdocs/` directories, which may contain sensitive enterprise data, are included in the `.gitignore` file. This prevents an accidental `git commit` from exposing this information. 