from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
import data
import auth
from models import Location, LocationsResponse, Stats

router = APIRouter(prefix="/v1", tags=["locations"])


def _paginate(items, limit, offset):
    return items[offset: offset + limit]


@router.get("/locations", response_model=LocationsResponse)
def get_locations(
    type: Optional[str] = Query(None, description="beach | river | waterfall"),
    ile: Optional[str] = Query(None, description="Grande-Terre, Basse-Terre, etc."),
    commune: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    _auth=Depends(auth.get_api_key),
):
    results = data.get_locations(type_=type, ile=ile, commune=commune)
    page = _paginate(results, limit, offset)
    return {"count": len(results), "data": page}


@router.get("/locations/{id}", response_model=Location)
def get_location(id: int, _auth=Depends(auth.get_api_key)):
    loc = data.get_location_by_id(id)
    if not loc:
        raise HTTPException(status_code=404, detail="Lieu introuvable.")
    return loc


@router.get("/beaches", response_model=LocationsResponse)
def get_beaches(
    ile: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    _auth=Depends(auth.get_api_key),
):
    results = data.get_locations(type_="beach", ile=ile)
    return {"count": len(results), "data": _paginate(results, limit, offset)}


@router.get("/rivers", response_model=LocationsResponse)
def get_rivers(
    ile: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    _auth=Depends(auth.get_api_key),
):
    results = data.get_locations(type_="river", ile=ile)
    return {"count": len(results), "data": _paginate(results, limit, offset)}


@router.get("/waterfalls", response_model=LocationsResponse)
def get_waterfalls(
    ile: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    _auth=Depends(auth.get_api_key),
):
    results = data.get_locations(type_="waterfall", ile=ile)
    return {"count": len(results), "data": _paginate(results, limit, offset)}


@router.get("/stats", response_model=Stats)
def get_stats(_auth=Depends(auth.get_api_key)):
    return data.get_stats()
