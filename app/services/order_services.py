from sqlalchemy.orm import Session

from app.models.order import OrderCreate, Order


def create_order(db: Session, order: OrderCreate):
    order = Order(user_id=order.user_id,
                  status=order.status,)