# RAG Deepmind Ai — Full Project Overview

A comprehensive **Retrieval-Augmented Generation (RAG)** ecosystem designed for document-grounded Q&A. This system consists of a high-performance **Node.js API Gateway** for orchestration and a specialized **Python RAG Microservice** for AI-driven retrieval and generation.

## Overview

Users often work with large PDF documents where extracting specific information is time-consuming. This system provides a seamless end-to-end pipeline:
- **Node.js Gateway:** Handles file uploads, job queuing ([BullMQ](https://docs.bullmq.io/)), and user-facing REST APIs.
- **Python Service:** Dedicated AI engine using [Google Gemini](https://ai.google.dev/) for embeddings/generation and [ChromaDB](https://docs.trychroma.com/) for vector storage.
- **Grounded Accuracy:** Answers are strictly based on retrieved document chunks to minimize hallucinations.

## Full System Architecture

```text
       [ Client (Web UI / Curl) ]
                │
                ▼ (HTTP - /api/upload, /api/search)
┌───────────────────────────────────────────┐
│           MAIN API GATEWAY (Node.js)      │
│   (Express, BullMQ, Redis, Multer)        │
└─────────────────────┬─────────────────────┘
                      │
                      ▼ (Internal REST - /api/v1/ask)
┌───────────────────────────────────────────┐
│           PYTHON RAG MICROSERVICE         │
│   (FastAPI, RAG Engine, Gemini, ChromaDB) │
└───────────┬───────────────────┬───────────┘
            │                   │
            ▼                   ▼
     ┌─────────────┐     ┌─────────────┐
     │   Redis     │     │  ChromaDB   │
     │  (Queues)   │     │  (Vectors)  │
     └─────────────┘     └─────────────┘
```

## Key Features

- **Decoupled Design:** Independent scaling of ingestion (Node.js) and inference (Python).
- **Asynchronous Processing:** Multi-threaded PDF parsing via [BullMQ](https://docs.bullmq.io/) background workers.
- **Semantic Search:** Advanced vector retrieval using `text-embedding-004`.
- **Tenant Isolation:** Secure multi-tenant data segregation supporting both `snake_case` and `camelCase` parameters.
- **Modern UI:** Built-in web interface for simple document management.

---

## 1. Main API Gateway (Node.js)

Located in `d:\RAGpractice`, this component serves as the entry point.

### Responsibilities:
- **File Management:** PDF upload and temporary storage.
- **Job Ingestion:** Pushes parsing tasks to [Redis](https://redis.io/) via BullMQ.
- **Background Workers:** Extracts text and interacts with the Python service for indexing.
- **Search Orchestration:** Coordinates between the user and the AI engine.

### External Resources:
- [Express.js Documentation](https://expressjs.com/)
- [BullMQ Guide](https://docs.bullmq.io/)
- [Redis Command Reference](https://redis.io/commands/)

---

## 2. Python RAG Microservice

Located in `d:\pyhon-rag-service`, this component handles the core AI logic.

### Responsibilities:
- **Vector Operations:** Manages document indexing and retrieval using [ChromaDB](https://docs.trychroma.com/).
- **LLM Orchestration:** Prompts [Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/flash/) with retrieved context.
- **API Security:** Protected via `X-Internal-API-Key` shared secret.

### External Resources:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Google Gemini API Reference](https://ai.google.dev/api/rest)

---

## Prerequisites

- **Python 3.10+** & **Node.js 18+**
- **Docker** (recommended for Redis/ChromaDB)
- **Google Gemini API Key** (Get one at [Google AI Studio](https://aistudio.google.com/))

## Installation & Setup

### 1. Infrastructure (Launch Dependencies)
```bash
# Start Redis (port 6379)
redis-server

# Start ChromaDB (port 8081)
chroma run --host localhost --port 8081
```

### 2. Python RAG Service
```bash
cd python-rag-service
python -m venv venv
source venv/Scripts/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
# Run service
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. Node.js API Gateway
```bash
cd RAGpractice
npm install
# Terminal 1: API Server
npm run dev
# Terminal 2: Background Worker
npm run worker
```

## API Reference

### Gateway API (Node.js)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload a PDF. Returns a `jobId`. |
| `POST` | `/api/search` | Ask a question. Body: `{"query": "..."}` |
| `GET`  | `/api/health` | Gateway health check. |

### Microservice API (Python)

#### `POST /api/v1/ask`
Performs semantic search and generates an answer.

- **Headers:** `X-Internal-API-Key: <secret>`
- **Request Body:**
  ```json
  {
    "question": "What is the summary?",
    "tenantId": "user_123"
  }
  ```
- **Response:**
  ```json
  {
    "answer": "The document states...",
    "sources": [{"filename": "doc.pdf", "pageNumber": 5}]
  }
  ```

## Configuration (.env)

Ensure both services have a `.env` file in their respective roots.

**Python Service (`.env`):**
```env
GEMINI_API_KEY=your_key
INTERNAL_API_KEY=shared_secret
CHROMA_HOST=localhost
CHROMA_PORT=8081
```

**Node.js Gateway (`.env`):**
```env
PORT=3000
GEMINI_API_KEY=your_key
INTERNAL_API_KEY=shared_secret
PYTHON_SERVICE_URL=http://localhost:8000
```

## Design Decisions (Advanced RAG)

This system implements **Advanced RAG** rather than traditional keyword search:
1. **Grounding:** LLMs act as language generators, not knowledge sources. Answers are strictly based on retrieved chunks.
2. **Context Preservation:** Strategic chunking with 10% overlap ensures semantic meaning isn't lost at boundaries.
3. **Hallucination Guard:** If no relevant chunks are found, the system explicitly returns "No relevant information found."

## Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Gateway** | [Node.js](https://nodejs.org/), [Express](https://expressjs.com/), [BullMQ](https://docs.bullmq.io/) |
| **AI Engine** | [FastAPI](https://fastapi.tiangolo.com/), [Python](https://www.python.org/) |
| **Storage** | [ChromaDB](https://docs.trychroma.com/), [Redis](https://redis.io/) |
| **Model** | [Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/flash/) |

## License

ISC
