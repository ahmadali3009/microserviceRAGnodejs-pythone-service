import google.generativeai as genai
from typing import Dict, Any, List, Tuple

from app.services.retriever import Retriever
from app.core.config import settings


class RAGEngine:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name=settings.GEMINI_ANSWER_MODEL)

    async def generate_answer(self, query: str) -> Tuple[str, List[str]]:
        """
        Retrieve relevant documents from ChromaDB and use Gemini to generate an answer.
        Returns (answer_text, list_of_sources).
        """
        docs = await self.retriever.retrieve(query)

        if not docs:
            return (
                "I could not find any relevant information in the knowledge base to answer your question.",
                [],
            )

        # Build context with numbered sources for the prompt
        context_parts = []
        sources = []
        for i, doc in enumerate(docs, start=1):
            source_name = doc.get("source", "unknown")
            context_parts.append(f"[Source {i}] (File: {source_name})\n{doc['text']}\n")
            if source_name not in sources:
                sources.append(source_name)

        context_text = "\n".join(context_parts)

        # Ported prompt logic from the previous Node.js implementation
        prompt = f"""
<SYSTEM_INSTRUCTIONS>
You are an expert business analyst.
Answer the user's question using ONLY the provided context sources below and also make the information more understandble to the user AND well structured.

IMPORTANT: Every claim you make MUST be followed by the source number in brackets, like [1] or [2].
If multiple sources support a point, cite all of them, like [1][2].

If the information is not in the context, state that clearly and do not make up an answer.
Give a clear, concise, professional answer.
</SYSTEM_INSTRUCTIONS>

<CONTEXT_SOURCES>
{context_text}
</CONTEXT_SOURCES>

<USER_QUESTION>
{query}
</USER_QUESTION>

<FINAL_RESPONSE_CHECK>
Ensure you have cited sources and did not use outside knowledge.
</FINAL_RESPONSE_CHECK>
"""

        try:
            response = await self.model.generate_content_async(prompt)
            answer_text = response.text
            return answer_text, sources
        except Exception as e:
            return f"Error generating answer: {str(e)}", sources
