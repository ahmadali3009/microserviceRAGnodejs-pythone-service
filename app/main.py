from fastapi import FastAPI
from app.api.routes import ask

app = FastAPI(title="RAG Service API")

app.include_router(ask.router, prefix="/api/v1", tags=["RAG"])

@app.get("/")
async def root():
    return {"message": "RAG service running"}