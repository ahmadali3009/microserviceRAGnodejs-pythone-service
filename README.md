# RAG Practice — PDF Document Q&A (Microservice Layer)

A **Retrieval-Augmented Generation (RAG)** system built as a dedicated **microservice layer**. It allows you to ask natural-language questions about your PDF documents and get accurate, document-grounded answers without reading entire files. 

By operating as an independent microservice, this project can be seamlessly integrated into larger applications or architectures, decoupling the heavy lifting of document processing, vector embeddings, and LLM orchestration from your main backend.

## Overview

Users often work with large PDF documents (50–100+ pages) such as resumes, reports, or manuals. Extracting specific information typically requires manual reading or keyword search—which is time-consuming, error-prone, and inefficient. This microservice solves that by:

- **Extracting text** from uploaded PDFs  
- **Chunking** content with configurable overlap  
- **Generating embeddings** via Google Gemini  
- **Storing vectors** in ChromaDB  
- **Retrieving relevant chunks** at query time  
- **Generating answers** grounded in retrieved context  

Answers are strictly based on document content to minimize hallucination.

## Features

- **Microservice API:** Fully decoupled REST API for easy integration with other services.
- **Asynchronous Processing:** Powered by BullMQ + Redis for non-blocking background document parsing.
- Semantic search over document chunks.
- LLM-powered answers using only retrieved context.
- Configurable chunk size, overlap, and batch size.

## Architecture

This project acts as an isolated RAG processing layer. It exposes a RESTful interface for external applications/clients while internally managing the message queues, vector search, and LLM communication.

```text
                  [ External Application / Client ]
                                 │
                                 ▼ (HTTP REST APIs)
┌───────────────────────────────────────────────────────────────┐
│                    RAG MICROSERVICE LAYER                     │
│                                                               │
│   POST /api/upload                        POST /api/search    │
│  ┌─────────────┐                         ┌─────────────┐      │
│  │  Express    │ ────────(PDF Jobs)────▶ │  BullMQ     │      │
│  │  Server     │                         │  Queue      │      │
│  └──────┬──────┘                         └──────┬──────┘      │
│         │                                       │             │
│         ▼                                       ▼             │
│  ┌─────────────┐                         ┌─────────────┐      │
│  │   Gemini    │ ◀──────(Query)───────── │  Worker     │      │
│  │   (LLM)     │                         │  (chunk +   │      │
│  └──────┬──────┘                         │   embed)    │      │
│         │                                └──────┬──────┘      │
│         │          ┌─────────────┐              │             │
│         └────────▶ │  ChromaDB   │ ◀────────────┘             │
│                    │  (vectors)  │                            │
│                    └─────────────┘                            │
└───────────────────────────────────────────────────────────────┘
                     │
              ┌──────┴──────┐
              │   Redis     │ (queue state)
              └─────────────┘
```

## Prerequisites

- **Node.js** 18+  
- **Redis** (for BullMQ)  
- **ChromaDB** (vector database)  
- **Google Gemini API key**  

## Installation

```bash
git clone <repository-url>
cd RAGpractice
npm install
```

## Configuration

Create a `.env` file in the project root:

```env
PORT=3000
GEMINI_API_KEY=your_google_gemini_api_key
```

## Running the System

You need three components running:

### 1. Redis

Ensure Redis is running locally on port 6379:

```bash
redis-server
```

### 2. ChromaDB

Run ChromaDB on port 8081 (default):

```bash
chroma run --host localhost --port 8081
```

### 3. Application

**Terminal 1 — API server:**

```bash
npm start
# or for development with auto-reload:
npm run dev
```

**Terminal 2 — Background worker (PDF processing):**

```bash
npm run worker
```

The server runs at `http://localhost:3000` (or the configured `PORT`).

**Web UI:** Open `http://localhost:3000` in a browser to upload PDFs via the built-in UI (useful for testing the microservice standalone).

## API Reference

| Method | Endpoint       | Description                              |
|--------|----------------|------------------------------------------|
| GET    | `/`            | Upload UI (static test page)             |
| GET    | `/api/health`  | Health check — returns microservice status |
| POST   | `/api/upload`  | Upload a PDF file                        |
| POST   | `/api/search`  | Query documents with a natural-language question |

### Upload PDF

```bash
curl -X POST http://localhost:3000/api/upload \
  -F "file=@/path/to/document.pdf"
```

**Response:**
```json
{
  "success": true,
  "jobId": "1"
}
```

The worker processes the PDF in the background. Wait for processing to finish before searching.

### Search / Ask

```bash
curl -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the main findings in this report?"}'
```

**Response:**
```json
{
  "response": "Based on the document, the main findings are..."
}
```

## Tech Stack

| Component   | Technology                    |
|------------|-------------------------------|
| Runtime    | Node.js (ES Modules)          |
| Framework  | Express 5                     |
| Queue      | BullMQ + Redis                |
| Vector DB  | ChromaDB                      |
| Embeddings | Google Gemini `text-embedding-004` |
| LLM        | Google Gemini 2.5 Flash       |
| PDF Parse  | pdf-parse                     |

## Project Structure

```
RAGpractice/
├── index.js     # Express API server, upload & search routes
├── worker.js    # BullMQ worker — chunking, embedding, ChromaDB upsert
├── common.js    # ChromaDB client, Gemini embedding function
├── public/      # Static upload UI (same origin, no CORS)
│   ├── index.html
│   ├── style.css
│   └── app.js
├── package.json
├── decien.md    # Architecture & design decisions
└── README.md
```

## Design Decisions

See [`decien.md`](decien.md) for detailed notes on:

- **Microservice Segregation:** Why decoupled asynchronous tasks are preferred.
- Why RAG over fine-tuning.
- Advanced RAG vs traditional/agentic.
- Asynchronous processing with BullMQ.
- ChromaDB selection.
- Hallucination mitigation strategy.

## License

ISC
