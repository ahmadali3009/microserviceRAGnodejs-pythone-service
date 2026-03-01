from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "RAG Service"
    
    # Gemini API
    GEMINI_API_KEY: str
    GEMINI_EMBED_MODEL: str = "models/gemini-embedding-001"
    GEMINI_ANSWER_MODEL: str = "gemini-2.5-flash"
    
    # ChromaDB
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8081
    CHROMA_BASE_URL: str = ""  # Will be computed in __init__ if not provided

    @property
    def chroma_url(self) -> str:
        if self.CHROMA_BASE_URL:
            return self.CHROMA_BASE_URL
        return f"http://{self.CHROMA_HOST}:{self.CHROMA_PORT}"

    CHROMA_TENANT: str = "default_tenant"
    CHROMA_DATABASE: str = "default_database"
    CHROMA_COLLECTION_NAME: str = "rag_collection"
    
    # Security
    INTERNAL_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
