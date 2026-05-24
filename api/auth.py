from fastapi import Header, Query, Request, HTTPException
from typing import Optional
import database

FREE_LIMIT = 100
ANON_LIMIT = 10


async def get_api_key(
    request: Request,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    api_key: Optional[str] = Query(None),
):
    key = x_api_key or api_key

    if not key:
        ip = request.client.host if request.client else "unknown"
        count = database.get_anon_requests(ip)
        if count >= ANON_LIMIT:
            raise HTTPException(
                status_code=429,
                detail=f"Limite anonyme atteinte ({ANON_LIMIT} req/jour). Obtenez une clé gratuite via POST /v1/keys/register",
            )
        database.increment_anon(ip)
        return {"key": None, "tier": "anonymous", "email": None}

    record = database.get_key(key)
    if not record:
        raise HTTPException(status_code=401, detail="Clé API invalide ou révoquée.")

    if record["tier"] == "premium":
        database.increment_requests(key)
        return record

    # Free tier
    if record["requests_today"] >= FREE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Limite free atteinte ({FREE_LIMIT} req/jour). Passez en premium pour un accès illimité.",
        )
    database.increment_requests(key)
    return record


async def require_admin(x_api_key: Optional[str] = Header(None, alias="X-API-Key")):
    import os
    admin_key = os.getenv("ADMIN_KEY", "")
    if not admin_key or x_api_key != admin_key:
        raise HTTPException(status_code=403, detail="Accès admin requis.")
