from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class AskRequest(BaseModel):
    question: str
    tenant_id: str = Field(..., alias="tenantId")
    context: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)

class AskResponse(BaseModel):
    answer: str
    sources: List[dict] = []
