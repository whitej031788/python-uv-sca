from typing import Optional
from fastapi import Header, HTTPException


def extract_bearer_token(authorization: Optional[str]) -> Optional[str]:
    """Extract token from Authorization header. Accepts Bearer or raw tokens."""
    if not authorization:
        return None
    value = authorization.strip()
    if value.lower().startswith("bearer "):
        return value[7:].strip()
    return value or None


async def require_auth(authorization: Optional[str] = Header(default=None)) -> str:
    """FastAPI dependency that ensures Authorization header is present."""
    token = extract_bearer_token(authorization)
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    return token
