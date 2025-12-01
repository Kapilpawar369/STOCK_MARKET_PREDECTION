import uuid
from typing import List

from sqlalchemy.orm import Session
import stripe

from app.models.payment import Payment, PaymentStatus, PaymentProvider
from app.schemas.payment import (
    PaymentCreate,
    PaymentOut,
    StripeCheckoutCreate,
    StripeCheckoutResponse,
)
from app.core.config import get_settings
from app.core.exceptions import CustomError

settings = get_settings()
stripe.api_key = settings.STRIPE_SECRET_KEY  # ✅ Stripe ko init karo


class PaymentService:
    def __init__(self, db: Session):
        self.db = db

    # ─────────────────────────────────────────────
    # LIST PAYMENTS FOR CURRENT USER
    # ─────────────────────────────────────────────
    def list_payments(self, user_id: str) -> List[PaymentOut]:
        if not user_id:
            raise CustomError("User ID is required", 400)

        payments = (
            self.db.query(Payment)
            .filter(Payment.user_id == user_id)
            .order_by(Payment.created_at.desc())
            .all()
        )

        return [
            PaymentOut(
                id=p.id,
                amount=float(p.amount),
                currency=p.currency,
                status=p.status.value if isinstance(p.status, PaymentStatus) else str(p.status),
                provider=p.provider.value if isinstance(p.provider, PaymentProvider) else str(p.provider),
                provider_order_id=p.provider_order_id,
            )
            for p in payments
        ]

    # ─────────────────────────────────────────────
    # SIMPLE LOCAL PAYMENT (no gateway) – OPTIONAL
    # ─────────────────────────────────────────────
    def create_local_payment(self, user_id: str, payload: PaymentCreate) -> PaymentOut:
        if not user_id:
            raise CustomError("User ID is required", 400)

        if payload.amount is None or payload.amount <= 0:
            raise CustomError("Payment amount must be greater than zero", 400)

        if not payload.currency or not payload.currency.strip():
            raise CustomError("Currency is required", 400)

        payment = Payment(
            id=str(uuid.uuid4()),
            user_id=user_id,
            amount=payload.amount,
            currency=payload.currency.upper(),
            status=PaymentStatus.CREATED,
            provider=PaymentProvider.STRIPE,
        )

        self.db.add(payment)

        try:
            self.db.commit()
            self.db.refresh(payment)
        except Exception as e:
            self.db.rollback()
            raise CustomError(
                f"Payment creation failed: {str(e)}",
                500
            )

        return PaymentOut(
            id=payment.id,
            amount=float(payment.amount),
            currency=payment.currency,
            status=payment.status.value,
            provider=payment.provider.value,
            provider_order_id=payment.provider_order_id,
        )

    # ─────────────────────────────────────────────
    # STEP 1: CREATE STRIPE CHECKOUT SESSION
    # ─────────────────────────────────────────────
    def create_stripe_checkout(
        self,
        user_id: str,
        payload: StripeCheckoutCreate,
    ) -> StripeCheckoutResponse:
        if not user_id:
            raise CustomError("User ID is required", 400)

        if payload.quantity <= 0:
            raise CustomError("Quantity must be greater than zero", 400)

        if payload.price_per_unit <= 0:
            raise CustomError("Price per unit must be greater than zero", 400)

        total_amount = payload.quantity * payload.price_per_unit

        # 1️Create payment row in DB
        payment = Payment(
            id=str(uuid.uuid4()),
            user_id=user_id,
            amount=total_amount,
            currency=payload.currency.upper(),
            status=PaymentStatus.CREATED,
            provider=PaymentProvider.STRIPE,
        )
        self.db.add(payment)
        try:
            self.db.commit()
            self.db.refresh(payment)
        except Exception as e:
            self.db.rollback()
            raise CustomError(f"Failed to create local payment: {str(e)}", 500)

        # 2️⃣ Create Stripe Checkout Session
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="payment",
                client_reference_id=user_id,  # ⭐ important for mapping user
                line_items=[
                    {
                        "price_data": {
                            "currency": payload.currency.lower(),
                            "product_data": {
                                "name": f"Buy {payload.symbol} x {payload.quantity}",
                            },
                            "unit_amount": int(payload.price_per_unit * 100),  # paise
                        },
                        "quantity": payload.quantity,
                    }
                ],
                metadata={
                    "payment_id": payment.id,
                    "symbol": payload.symbol,
                    "quantity": str(payload.quantity),
                },
                success_url="http://localhost:8000/frontend/payment-success.html?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://localhost:8000/frontend/payment-cancelled.html",
            )
        except Exception as e:
            # Stripe failure → local payment ko FAILED mark karo
            payment.status = PaymentStatus.FAILED
            self.db.commit()
            raise CustomError(f"Stripe session creation failed: {str(e)}", 500)

        # 3Stripe session id ko DB me store karo
        payment.provider_order_id = session.id
        try:
            self.db.commit()
            self.db.refresh(payment)
        except Exception:
            self.db.rollback()
            # Even if DB update fails, we can still return session link
            pass

        return StripeCheckoutResponse(
            checkout_url=session.url,
            session_id=session.id,
        )

    # ─────────────────────────────────────────────
    # STEP 2: HANDLE STRIPE WEBHOOK
    # ─────────────────────────────────────────────
    def handle_stripe_webhook(self, payload: bytes, sig_header: str):
        if not settings.STRIPE_WEBHOOK_SECRET:
            raise CustomError("Stripe webhook secret not configured", 500)

        import stripe

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET,
            )
        except stripe.error.SignatureVerificationError:
            raise CustomError("Invalid Stripe signature", 400)
        except ValueError:
            raise CustomError("Invalid payload", 400)

        # We only care about checkout.session.completed
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]

            payment_id = session.get("metadata", {}).get("payment_id")
            user_id = session.get("client_reference_id")
            payment_intent = session.get("payment_intent")

            if not payment_id:
                raise CustomError("Payment ID missing in Stripe metadata", 400)

            payment: Payment | None = (
                self.db.query(Payment)
                .filter(Payment.id == payment_id)
                .first()
            )

            if not payment:
                raise CustomError("Local payment not found", 400)

            # Optional extra safety: ensure the same user
            if user_id and payment.user_id != user_id:
                raise CustomError("Payment does not belong to this user", 400)

            payment.status = PaymentStatus.SUCCESS
            payment.provider_payment_id = payment_intent

            try:
                self.db.commit()
            except Exception:
                self.db.rollback()
                raise CustomError("Failed to update payment after webhook", 500)

        # You can log other event types if needed

        return {"ok": True}
