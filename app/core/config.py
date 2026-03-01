from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "RAG Service"
    
    # Gemini API
    GEMINI_API_KEY: str
    GEMINI_EMBED_MODEL: str = "models/gemini-embedding-001"
    GEMINI_ANSWER_MODEL: str = "gemini-2.5-flash"
    
    # ChromaDB
    CHROMA_BASE_URL: str = "http://localhost:8081"
    CHROMA_TENANT: str = "default_tenant"
    CHROMA_DATABASE: str = "default_database"
    CHROMA_COLLECTION_NAME: str = "rag_collection"
    
    # Security
    INTERNAL_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
