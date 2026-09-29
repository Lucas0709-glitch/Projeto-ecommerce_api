from sqlalchemy.orm import Session

from app.models.order import Order
from app.schemas.order import OrderCreate


def create_order(db: Session, order: OrderCreate):
    db_order = Order(
        usuario_id=order.usuario_id,
        status="aberto",
        total=0
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order