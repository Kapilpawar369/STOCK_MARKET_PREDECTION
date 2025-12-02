# app/services/order_service.py
import uuid
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatus
from app.models.payment import Payment, PaymentStatus
from app.models.stock import Stock
from app.schemas.order import OrderCreate, OrderOut
from app.core.exceptions import CustomError


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    # ─────────────────────────────────────────────
    # CREATE BUY ORDER
    # ─────────────────────────────────────────────
    def create_order(self, user_id: str, payload: OrderCreate) -> OrderOut:
        if not user_id:
            raise CustomError("User ID is required", 400)

        # 1) Basic validations
        if not payload.symbol or not payload.symbol.strip():
            raise CustomError("Stock symbol is required", 400)

        if payload.quantity <= 0:
            raise CustomError("Quantity must be greater than zero", 400)

        if payload.price_per_unit <= 0:
            raise CustomError("Price per unit must be greater than zero", 400)

        symbol = payload.symbol.upper()

        # 2) Check stock exists (optional but good)
        stock = (
            self.db.query(Stock)
            .filter(Stock.symbol == symbol)
            .first()
        )

        if not stock:
            raise CustomError("Invalid stock symbol", 400)

        # 3) If payment_id provided → validate payment
        payment: Optional[Payment] = None

        if payload.payment_id:
            payment = (
                self.db.query(Payment)
                .filter(
                    Payment.id == payload.payment_id,
                    Payment.user_id == user_id,
                )
                .first()
            )

            if not payment:
                raise CustomError("Payment not found for this user", 400)

            # REAL PRODUCTION: payment must be SUCCESS
            if payment.status != PaymentStatus.SUCCESS:
                raise CustomError("Payment is not successful yet", 400)

        # 4) Compute total price
        total_price = Decimal(str(payload.price_per_unit)) * Decimal(
            payload.quantity
        )

        # 5) Create order
        order = Order(
            id=str(uuid.uuid4()),
            user_id=user_id,
            symbol=symbol,
            quantity=payload.quantity,
            price_per_unit=Decimal(str(payload.price_per_unit)),
            total_price=total_price,
            currency=payload.currency.upper(),
            status=OrderStatus.COMPLETED
            if payment
            else OrderStatus.PENDING,
            payment_id=payment.id if payment else None,
        )

        self.db.add(order)

        try:
            self.db.commit()
            self.db.refresh(order)
        except Exception as e:
            self.db.rollback()
            raise CustomError(
                f"Failed to create order: {str(e)}",
                500,
            )

        return OrderOut(
            id=order.id,
            symbol=order.symbol,
            quantity=order.quantity,
            price_per_unit=float(order.price_per_unit),
            total_price=float(order.total_price),
            currency=order.currency,
            status=order.status.value if isinstance(order.status, OrderStatus) else str(order.status),
            payment_id=order.payment_id,
            created_at=order.created_at,
        )

    # ─────────────────────────────────────────────
    # LIST ORDERS FOR CURRENT USER
    # ─────────────────────────────────────────────
    def list_orders(self, user_id: str) -> List[OrderOut]:
        if not user_id:
            raise CustomError("User ID is required", 400)

        orders = (
            self.db.query(Order)
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .all()
        )

        return [
            OrderOut(
                id=o.id,
                symbol=o.symbol,
                quantity=o.quantity,
                price_per_unit=float(o.price_per_unit),
                total_price=float(o.total_price),
                currency=o.currency,
                status=o.status.value if isinstance(o.status, OrderStatus) else str(o.status),
                payment_id=o.payment_id,
                created_at=o.created_at,
            )
            for o in orders
        ]
