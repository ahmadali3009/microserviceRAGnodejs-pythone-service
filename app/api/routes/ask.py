import logging
from fastapi import APIRouter, HTTPException, Depends

from app.schemas import AskRequest, AskResponse
from app.services.vector_store import VectorStore
from app.services.splitter import TextSplitter
from app.services.retriever import Retriever
from app.services.rag_engine import RAGEngine
from app.api.deps import verify_internal_api_key

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services once at module load
_vector_store = VectorStore()
_splitter = TextSplitter()
_retriever = Retriever(vector_store=_vector_store, splitter=_splitter)
_rag_engine = RAGEngine(retriever=_retriever)


@router.post("/ask", response_model=AskResponse, dependencies=[Depends(verify_internal_api_key)])
async def ask_question(request: AskRequest):
    """
    Receive a question from the frontend, perform semantic search
    over ChromaDB using Gemini embeddings, and return the answer with sources.
    """
    try:
        logger.info(f"Received question: {request.question} for tenant: {request.tenant_id}")
        answer, sources = await _rag_engine.generate_answer(request.question, request.tenant_id, request.context)
        return AskResponse(answer=answer, sources=sources)
    except Exception as e:
        logger.error(f"RAG pipeline error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
