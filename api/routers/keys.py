from fastapi import APIRouter, Depends, HTTPException
import database
import auth
from models import KeyRegisterRequest, KeyRegisterResponse, KeyInfo

router = APIRouter(prefix="/v1/keys", tags=["api-keys"])


@router.post("/register", response_model=KeyRegisterResponse)
def register_key(body: KeyRegisterRequest):
    key = database.create_key(email=body.email, name=body.name)
    return {
        "key": key,
        "tier": "free",
        "daily_limit": 100,
        "message": (
            "Clé créée avec succès. Incluez-la dans vos requêtes via l'en-tête "
            "X-API-Key ou le paramètre ?api_key=. "
            "Pour passer en premium (illimité), contactez-nous."
        ),
    }


@router.get("/me", response_model=KeyInfo)
def get_my_key(current=Depends(auth.get_api_key)):
    if not current.get("key"):
        raise HTTPException(status_code=401, detail="Clé API requise.")
    record = database.get_key(current["key"])
    if not record:
        raise HTTPException(status_code=404, detail="Clé introuvable.")
    daily_limit = -1 if record["tier"] == "premium" else 100
    return {**record, "daily_limit": daily_limit}
