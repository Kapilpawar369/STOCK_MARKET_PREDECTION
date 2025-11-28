from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.order import Order, OrderStatus
from app.models.stock import Stock
from app.models.payment import Payment
from app.schemas.order import OrderCreate, OrderOut, PortfolioItem
from app.core.exceptions import CustomError


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    # ─────────────────────────────────────────
    # CREATE ORDER AFTER SUCCESSFUL PAYMENT
    # ─────────────────────────────────────────
    def create_order(self, user_id: str, payload: OrderCreate) -> OrderOut:
        if not user_id:
            raise CustomError("User ID is required", 400)

        # Basic validations
        if not payload.symbol or not payload.symbol.strip():
            raise CustomError("Stock symbol is required", 400)

        if payload.quantity <= 0:
            raise CustomError("Quantity must be greater than zero", 400)

        # Check payment exists
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

        # Optional: Ensure payment is successful
        if str(payment.status) != "SUCCESS":
            raise CustomError("Payment is not successful yet", 400)

        symbol = payload.symbol.upper()

        # Optional: validate stock exists in our DB
        stock = (
            self.db.query(Stock)
            .filter(Stock.symbol == symbol)
            .first()
        )
        if not stock:
            raise CustomError("Stock not found in system", 400)

        total_price = payload.quantity * payload.price_per_unit

        order = Order(
            user_id=user_id,
            symbol=symbol,
            quantity=payload.quantity,
            price_per_unit=payload.price_per_unit,
            total_price=total_price,
            currency=payload.currency.upper(),
            status=OrderStatus.COMPLETED,   # because payment already done
            payment_id=payload.payment_id,
        )

        self.db.add(order)

        try:
            self.db.commit()
            self.db.refresh(order)
        except Exception:
            self.db.rollback()
            raise CustomError("Failed to create order", 500)

        return OrderOut(
            id=order.id,
            symbol=order.symbol,
            quantity=order.quantity,
            price_per_unit=order.price_per_unit,
            total_price=order.total_price,
            currency=order.currency,
            status=order.status.value,
            created_at=order.created_at,
        )

    # ─────────────────────────────────────────
    # LIST ALL ORDERS OF CURRENT USER
    # ─────────────────────────────────────────
    def list_orders(self, user_id: str) -> List[OrderOut]:
        if not user_id:
            raise CustomError("User ID is required", 400)

        items = (
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
                price_per_unit=o.price_per_unit,
                total_price=o.total_price,
                currency=o.currency,
                status=o.status.value,
                created_at=o.created_at,
            )
            for o in items
        ]

    # ─────────────────────────────────────────
    # PORTFOLIO VIEW (AGGREGATED HOLDINGS)
    # ─────────────────────────────────────────
    def get_portfolio(self, user_id: str) -> List[PortfolioItem]:
        if not user_id:
            raise CustomError("User ID is required", 400)

        rows = (
            self.db.query(
                Order.symbol.label("symbol"),
                func.sum(Order.quantity).label("total_quantity"),
                func.sum(Order.total_price).label("total_invested"),
            )
            .filter(
                Order.user_id == user_id,
                Order.status == OrderStatus.COMPLETED,
            )
            .group_by(Order.symbol)
            .all()
        )

        portfolio: List[PortfolioItem] = []

        for row in rows:
            if row.total_quantity == 0:
                continue

            avg_buy_price = row.total_invested / row.total_quantity

            portfolio.append(
                PortfolioItem(
                    symbol=row.symbol,
                    total_quantity=int(row.total_quantity),
                    avg_buy_price=round(avg_buy_price, 2),
                    total_invested=round(row.total_invested, 2),
                )
            )

        return portfolio
