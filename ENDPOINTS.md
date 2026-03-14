# Python RAG Microservice - API Endpoints

This document outlines the API endpoints exposed by the Python RAG (Retrieval-Augmented Generation) microservice. This service is built with FastAPI and acts as the secure AI engine for answering questions using semantic search over ChromaDB and Gemini embeddings.

## Base URL
All API v1 endpoints are prefixed with `/api/v1`. The root endpoint is available at `/`.

---

## Endpoints

### 1. Health Check (Root)
Check if the RAG service is running successfully.

- **URL:** `/`
- **Method:** `GET`
- **Auth Required:** No
- **Response:**
  ```json
  {
    "message": "RAG service running"
  }
  ```

---

### 2. Ask Question (RAG Pipeline)
Receive a question, perform semantic search over the vectorized documents, and generate an answer using the LLM with the retrieved context.

- **URL:** `/api/v1/ask`
- **Method:** `POST`
- **Auth Required:** Yes (Internal API Key via Headers)
- **Headers:**
  - `X-Internal-Secret`: The shared internal secret key between the Gateway and this service.
- **Request Body:**
  ```json
  {
    "question": "What is the company's leave policy?",
    "tenant_id": "tenant_abc_123"
  }
  ```
  *Note: Both `tenant_id` (snake_case) and `tenantId` (camelCase) are supported.*
- **Response:**
  ```json
  {
    "answer": "According to the company handbook...",
    "sources": [
      {
        "id": 1,
        "filename": "Employee_Handbook.pdf",
        "pageNumber": 12,
        "chunkIndex": 45,
        "viewUrl": "..."
      }
    ]
  }
  ```

## Internal Architecture Note
This service initializes the following internal components on startup:
1. **VectorStore:** Manages the ChromaDB instance.
2. **TextSplitter:** Handles text chunking.
3. **Retriever:** Orchestrates search combining VectorStore and TextSplitter.
4. **RAGEngine:** Coordinates the generation of answers using the Retriever context and LLM.
