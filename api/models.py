from pydantic import BaseModel, EmailStr
from typing import Optional


class Location(BaseModel):
    id: int
    nom: str
    type: str
    commune: str
    code_postal: str
    ile: str
    lat: float
    lon: float


class LocationsResponse(BaseModel):
    count: int
    data: list[Location]


class Stats(BaseModel):
    total: int
    beaches: int
    rivers: int
    waterfalls: int
    by_island: dict[str, int]
    last_updated: str


class KeyRegisterRequest(BaseModel):
    email: str
    name: str


class KeyInfo(BaseModel):
    key: str
    email: str
    name: str
    tier: str
    created_at: str
    requests_today: int
    daily_limit: int


class KeyRegisterResponse(BaseModel):
    key: str
    tier: str
    daily_limit: int
    message: str
