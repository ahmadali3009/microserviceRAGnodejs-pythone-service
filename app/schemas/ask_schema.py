from pydantic import BaseModel
from typing import List, Optional

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = []
