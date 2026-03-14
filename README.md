# RAG Microservice — Python RAG Service

A **Retrieval-Augmented Generation (RAG)** system built as a dedicated **Python microservice**. It enables natural-language questioning over PDF documents, providing document-grounded answers by leveraging semantic search and large language models.

By operating as an independent microservice, this project decouples document processing, vector embeddings, and LLM orchestration from the main application logic, offering a scalable and maintainable AI layer.

## Overview

This microservice handles the core RAG pipeline:
- **Semantic Retrieval:** Uses Google Gemini embeddings and ChromaDB for efficient vector search.
- **Contextual Generation:** Grounded answers generated via Google Gemini, strictly based on retrieved document chunks.
- **Tenant Isolation:** Supports multi-tenant data segregation.
- **FastAPI Framework:** High-performance, asynchronous REST API.

## Features

- **Decoupled Architecture:** Easily integrable into any system via RESTful APIs.
- **Semantic Search:** Advanced document retrieval using state-of-the-art embeddings.
- **Grounded Answers:** Minimizes hallucinations by strictly utilizing retrieved context.
- **Secure Integration:** Protected by internal API keys.

## Architecture

This service acts as the AI engine in a microservice ecosystem.

```text
                   [ API Gateway / Main Backend ]
                                  │
                                  ▼ (HTTP REST - /api/v1/ask)
┌───────────────────────────────────────────────────────────────┐
│                    PYTHON RAG MICROSERVICE                    │
│                                                               │
│   ┌─────────────┐          ┌──────────────────────────┐       │
│   │  FastAPI    │ ───────▶ │   RAG Engine             │       │
│   │  Router     │          │ (Retriever + LLM)        │       │
│   └──────┬──────┘          └────────────┬─────────────┘       │
│          │                              │                     │
│          ▼                              ▼                     │
│   ┌─────────────┐          ┌──────────────────────────┐       │
│   │  Gemini     │ ◀──────▶ │   ChromaDB               │       │
│   │  (LLM)      │          │   (Vector Store)         │       │
│   └─────────────┘          └──────────────────────────┘       │
└───────────────────────────────────────────────────────────────┘
```

## Prerequisites

- **Python 3.10+**
- **ChromaDB** running as a service (typically on port 8081)
- **Google Gemini API Key**

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd python-rag-service
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or
   source venv/bin/activate      # Linux/macOS
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_google_gemini_api_key
INTERNAL_API_KEY=your_secure_internal_api_key
CHROMA_HOST=localhost
CHROMA_PORT=8081
```

## Running the System

Ensure **ChromaDB** is running before starting the service:

```bash
chroma run --host localhost --port 8081
```

Start the FastAPI service:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The service will be available at `http://localhost:8000`.

## API Reference

### Ask Question

Performs semantic search and generates an answer based on document context.

- **URL:** `/api/v1/ask`
- **Method:** `POST`
- **Headers:**
  - `X-Internal-API-Key`: `<your_internal_api_key>`
  - `Content-Type`: `application/json`

- **Request Body:**
  ```json
  {
    "question": "What is the summary of the document?",
    "tenantId": "user_tenant_123"
  }
  ```

- **Response:**
  ```json
  {
    "answer": "The document provides a detailed overview of...",
    "sources": [
      {
        "filename": "document_name.pdf",
        "pageNumber": 5,
        "contentSnippet": "..."
      }
    ]
  }
  ```

See [ENDPOINTS.md](ENDPOINTS.md) for full API documentation.

## Tech Stack

| Component     | Technology                          |
|---------------|-------------------------------------|
| Framework     | FastAPI                             |
| Language      | Python 3.10+                        |
| Vector DB     | ChromaDB                            |
| Embeddings    | Google Gemini (`text-embedding-004`) |
| LLM           | Google Gemini 2.5 Flash             |
| Documentation | Pydantic (OpenAPI/Swagger)          |

## Project Structure

```
app/
├── api/             # API routes and dependencies
├── core/            # Configuration and core logic
├── schemas/         # Pydantic models (Request/Response)
├── services/        # RAG Engine, Vector Store, Splitter, etc.
└── main.py          # FastAPI application entry point
```

## License

ISC
