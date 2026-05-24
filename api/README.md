# Guadeloupe Waters API

API REST freemium pour les plages, rivières et cascades de Guadeloupe.

## Déploiement sur Coolify

1. Ajouter ce repo dans Coolify → New Resource → Git Repository
2. Définir le **Build Context** : `/` (racine du repo)
3. Définir le **Dockerfile Path** : `Dockerfile` (à la racine)
4. Copier `api/.env.example` → `api/.env` et remplir les variables :
   - `ADMIN_KEY` — clé secrète pour les endpoints admin
   - `STRIPE_WEBHOOK_SECRET` / `STRIPE_SECRET_KEY` — optionnel, pour le paiement
5. Déployer → l'API **et la carte** sont disponibles sur le port 8000

**URLs après déploiement :**
- `https://ton-domaine/` → carte Leaflet interactive
- `https://ton-domaine/v1/beaches` → API REST
- `https://ton-domaine/docs` → Swagger UI
- `https://ton-domaine/health` → healthcheck Coolify

## Endpoints principaux

```bash
# Toutes les plages
GET /v1/beaches

# Lieux filtrés par île
GET /v1/locations?type=beach&ile=Grande-Terre

# Stats
GET /v1/stats

# Obtenir une clé gratuite
POST /v1/keys/register
{"email": "vous@exemple.com", "name": "Mon App"}

# Info clé
GET /v1/keys/me   (X-API-Key: gw_xxx)
```

Documentation interactive : `http://votre-domaine/docs`

## Tiers

| Tier | Limite | Prix |
|------|--------|------|
| Anonyme | 10 req/jour par IP | Gratuit |
| Free | 100 req/jour | Gratuit (inscription email) |
| Premium | Illimité | Payant (Stripe) |

## Auth

Toutes les requêtes acceptent la clé via :
- En-tête : `X-API-Key: gw_votre_cle`
- Query param : `?api_key=gw_votre_cle`
