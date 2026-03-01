from typing import List, Dict, Any

from app.services.splitter import TextSplitter
from app.services.vector_store import VectorStore


class Retriever:
    def __init__(self, vector_store: VectorStore, splitter: TextSplitter):
        self.vector_store = vector_store
        self.splitter = splitter

    async def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Split the query into chunks, search ChromaDB for each chunk,
        and return deduplicated results ranked by best score.
        """
        chunks = self.splitter.split_text(query)
        if not chunks:
            chunks = [query]

        seen_texts = set()
        all_results: List[Dict[str, Any]] = []

        for chunk in chunks:
            results = await self.vector_store.search(chunk, k=top_k)
            for result in results:
                if result["text"] not in seen_texts:
                    seen_texts.add(result["text"])
                    all_results.append(result)

        # Sort by score descending and return top_k
        all_results.sort(key=lambda x: x["score"], reverse=True)
        return all_results[:top_k]
