import logging
import httpx
import google.generativeai as genai
from typing import List, Dict, Any, Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

# Add file handler for debugging if not exists
if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
    fh = logging.FileHandler("debug_rag.log")
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)


class VectorStore:
    def __init__(self):
        self.base_url = settings.chroma_url.rstrip("/")
        self.collection_name = settings.CHROMA_COLLECTION_NAME
        self.collection_id = None
        genai.configure(api_key=settings.GEMINI_API_KEY)

    async def _get_collection_id(self, client: httpx.AsyncClient) -> str:
        """Fetch the UUID of the collection from ChromaDB."""
        if self.collection_id:
            return self.collection_id

        # Updated URL path for ChromaDB v2 with tenants and databases
        url = f"{self.base_url}/api/v2/tenants/{settings.CHROMA_TENANT}/databases/{settings.CHROMA_DATABASE}/collections/{self.collection_name}"
        response = await client.get(url)
        if response.status_code == 200:
            self.collection_id = response.json()["id"]
            return self.collection_id
        else:
            logger.error(f"Failed to find ChromaDB collection '{self.collection_name}': {response.text}")
            raise Exception(f"Collection '{self.collection_name}' not found under tenant '{settings.CHROMA_TENANT}' and database '{settings.CHROMA_DATABASE}'.")

    async def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding using Gemini."""
        result = genai.embed_content(
            model=settings.GEMINI_EMBED_MODEL,
            content=text,
            task_type="retrieval_query",
        )
        return result["embedding"]

    async def search(self, query: str, tenant_id: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search ChromaDB via REST API."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                # 1. Get collection ID
                coll_id = await self._get_collection_id(client)

                # 2. Get embedding vector
                embedding = await self._get_embedding(query)

                # 3. Query ChromaDB
                # Updated URL path for ChromaDB v2 query
                query_url = f"{self.base_url}/api/v2/tenants/{settings.CHROMA_TENANT}/databases/{settings.CHROMA_DATABASE}/collections/{coll_id}/query"
                payload = {
                    "query_embeddings": [embedding],
                    "n_results": k,
                    "where": {"tenantId": tenant_id},
                    "include": ["documents", "metadatas", "distances"]
                }
                
                response = await client.post(query_url, json=payload)
                if response.status_code != 200:
                    logger.error(f"ChromaDB query failed: {response.text}")
                    return []

                results = response.json()
                logger.info(f"ChromaDB raw results: {results}")
                
                # Format response to match expected structure
                docs = results.get("documents", [[]])[0]
                metas = results.get("metadatas", [[]])[0]
                distances = results.get("distances", [[]])[0]

                output = []
                for doc, meta, dist in zip(docs, metas, distances):
                    # Align with original Node.js metadata structure
                    filename = meta.get("filename", "unknown") if meta else "unknown"
                    page_number = meta.get("pageNumber") if meta else None
                    source_str = f"{filename}" + (f", Page: {page_number}" if page_number else "")
                    
                    output.append({
                        "text": doc,
                        "source": source_str,
                        "metadata": meta,  # Include full metadata for frontend citation
                        "score": round(1 - dist, 4) if dist is not None else 0.0
                    })
                return output

            except Exception as e:
                logger.error(f"Vector search error: {e}")
                return []

    def add_documents(self, documents: List[str], metadatas: List[Dict] = None, ids: List[str] = None):
        """Placeholder - typically handled by the Node.js service."""
        pass
