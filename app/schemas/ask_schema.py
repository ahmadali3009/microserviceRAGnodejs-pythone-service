from pydantic import BaseModel
from typing import List, Optional

class AskRequest(BaseModel):
    question: str
    context: Optional[str] = None
    tenant_id: str

class AskResponse(BaseModel):
    answer: str
    sources: List[dict] = []
