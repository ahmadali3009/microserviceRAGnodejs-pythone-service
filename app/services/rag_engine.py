from typing import Dict, Any, List, Tuple

from app.services.retriever import Retriever


class RAGEngine:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    async def generate_answer(self, query: str) -> Tuple[str, List[str]]:
        """
        Retrieve relevant documents from ChromaDB and build the answer.
        Returns (answer_text, list_of_sources).
        """
        docs = await self.retriever.retrieve(query)

        if not docs:
            return (
                "I could not find any relevant information in the knowledge base.",
                [],
            )

        # Build answer from top retrieved docs
        context_parts = []
        sources = []
        for i, doc in enumerate(docs, start=1):
            context_parts.append(f"[{i}] {doc['text']}")
            source = doc.get("source", "unknown")
            if source not in sources:
                sources.append(source)

        context = "\n\n".join(context_parts)
        answer = (
            f"Based on the retrieved documents:\n\n{context}"
        )

        return answer, sources
