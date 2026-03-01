from fastapi import Header, HTTPException, status
from app.core.config import settings

async def verify_internal_api_key(x_internal_api_key: str = Header(...)):
    """
    Dependency to verify the internal API key sent in the request header.
    Expects 'X-Internal-API-Key' header.
    """
    if x_internal_api_key != settings.INTERNAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate internal service credentials",
        )
    return x_internal_api_key
