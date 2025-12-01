import stripe
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.models.payment import Payment, PaymentStatus

settings = get_settings()
stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter()


@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return {"status": "invalid signature"}

    # PAYMENT SUCCESS EVENT
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        payment_id = session["metadata"]["payment_id"]

        payment = db.query(Payment).filter(Payment.id == payment_id).first()

        if payment:
            payment.status = PaymentStatus.SUCCESS
            payment.provider_payment_id = session.get("payment_intent")
            db.commit()

    # PAYMENT FAILED EVENT
    elif event["type"] == "payment_intent.payment_failed":
        intent = event["data"]["object"]

        payment_id = intent["metadata"]["payment_id"]

        payment = db.query(Payment).filter(Payment.id == payment_id).first()

        if payment:
            payment.status = PaymentStatus.FAILED
            db.commit()

    return {"status": "success"}
