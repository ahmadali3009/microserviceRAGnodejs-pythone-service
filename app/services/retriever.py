import logging
from typing import List, Dict, Any

from app.services.splitter import TextSplitter
from app.services.vector_store import VectorStore

logger = logging.getLogger(__name__)

# Add file handler for debugging if not exists
if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
    fh = logging.FileHandler("debug_rag.log")
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)


class Retriever:
    def __init__(self, vector_store: VectorStore, splitter: TextSplitter):
        self.vector_store = vector_store
        self.splitter = splitter

    async def retrieve(self, query: str, tenant_id: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Split the query into chunks, search ChromaDB for each chunk,
        and return deduplicated results ranked by best score that meet the threshold.
        """
        MIN_SCORE = 0.3  # Lowered from 0.5 to be more inclusive of relevant matches
        
        chunks = self.splitter.split_text(query)
        if not chunks:
            chunks = [query]

        seen_texts = set()
        all_results: List[Dict[str, Any]] = []

        for chunk in chunks:
            results = await self.vector_store.search(chunk, tenant_id=tenant_id, k=top_k)
            for result in results:
                # Log score for debugging
                logger.info(f"Retrieved Result Score: {result['score']} | Content: {result['text'][:50]}...")
                
                # Only include results that meet the similarity threshold
                if result["score"] >= MIN_SCORE:
                    if result["text"] not in seen_texts:
                        seen_texts.add(result["text"])
                        all_results.append(result)
                else:
                    logger.debug(f"Result ignored (score {result['score']} < {MIN_SCORE})")

        # Sort by score descending and return top_k
        all_results.sort(key=lambda x: x["score"], reverse=True)
        return all_results[:top_k]
