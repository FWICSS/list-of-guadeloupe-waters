import os
from fastapi import APIRouter, Request, HTTPException

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/stripe")
async def stripe_webhook(request: Request):
    secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    stripe_key = os.getenv("STRIPE_SECRET_KEY", "")

    if not secret or not stripe_key:
        raise HTTPException(status_code=501, detail="Stripe non configuré.")

    try:
        import stripe
    except ImportError:
        raise HTTPException(status_code=501, detail="stripe SDK non installé.")

    stripe.api_key = stripe_key
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig, secret)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Signature Stripe invalide.")

    if event["type"] in ("checkout.session.completed", "invoice.payment_succeeded"):
        session = event["data"]["object"]
        api_key = session.get("metadata", {}).get("api_key")
        if api_key:
            import database
            database.upgrade_to_premium(api_key)

    return {"received": True}
