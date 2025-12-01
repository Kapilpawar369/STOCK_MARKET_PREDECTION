import stripe
from fastapi import APIRouter, Depends
from app.core.config import get_settings
from app.api.deps import get_current_user_id

settings = get_settings()
stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter()

@router.get("/payments/stripe/init")
def create_stripe_checkout(user_id: str = Depends(get_current_user_id)):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {"name": "Stock Purchase"},
                    "unit_amount": 50000,
                },
                "quantity": 1,
            }
        ],
        success_url="http://127.0.0.1:8000/frontend/payment-success.html?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://127.0.0.1:8000/frontend/payment-cancel.html",
    )

    return {"checkout_url": session.url}
