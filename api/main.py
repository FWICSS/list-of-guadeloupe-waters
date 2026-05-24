import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import data
import database
from routers import locations, keys, admin, webhooks

DOCS_DIR = os.getenv("DOCS_DIR", "/docs")


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    data.load()
    yield


app = FastAPI(
    title="Guadeloupe Waters API",
    description=(
        "API REST pour les plages, rivières et cascades de Guadeloupe.\n\n"
        "**Free tier** : 100 requêtes/jour — obtenez une clé via `POST /v1/keys/register`\n\n"
        "**Premium** : illimité — contactez-nous ou intégrez Stripe"
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

app.include_router(locations.router)
app.include_router(keys.router)
app.include_router(admin.router)
app.include_router(webhooks.router)


@app.get("/health", tags=["info"])
def health():
    return {"status": "ok"}


@app.get("/info", tags=["info"])
def root():
    stats = data.get_stats()
    return {
        "name": "Guadeloupe Waters API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "all_locations": "/v1/locations",
            "beaches": "/v1/beaches",
            "rivers": "/v1/rivers",
            "waterfalls": "/v1/waterfalls",
            "stats": "/v1/stats",
            "get_api_key": "POST /v1/keys/register",
        },
        "stats": stats,
        "github": "https://github.com/dimitriaigle/List_of_beaches_and_rivers_of_Guadeloupe",
    }


# Catch-all : sert la carte Leaflet + data.json + api statique
# Monté en dernier pour ne pas masquer les routes FastAPI
if os.path.isdir(DOCS_DIR):
    app.mount("/", StaticFiles(directory=DOCS_DIR, html=True), name="static")
