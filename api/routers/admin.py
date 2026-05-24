from fastapi import APIRouter, Depends, HTTPException
import database
import auth

router = APIRouter(prefix="/v1/admin", tags=["admin"])


@router.get("/keys")
def list_keys(_=Depends(auth.require_admin)):
    return database.list_keys()


@router.post("/keys/{key}/upgrade")
def upgrade_key(key: str, _=Depends(auth.require_admin)):
    record = database.get_key(key)
    if not record:
        raise HTTPException(status_code=404, detail="Clé introuvable.")
    database.upgrade_to_premium(key)
    return {"message": f"Clé {key} passée en premium."}


@router.delete("/keys/{key}")
def revoke_key(key: str, _=Depends(auth.require_admin)):
    record = database.get_key(key)
    if not record:
        raise HTTPException(status_code=404, detail="Clé introuvable.")
    database.revoke_key(key)
    return {"message": f"Clé {key} révoquée."}


@router.post("/reset-daily")
def reset_daily(_=Depends(auth.require_admin)):
    database.reset_daily_counts()
    return {"message": "Compteurs quotidiens réinitialisés."}
