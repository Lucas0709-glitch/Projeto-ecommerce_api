from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.order_item import OrderItem
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

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def update_order_total(db: Session, order_id: int):
    total = (
        db.query(
            func.sum(
                OrderItem.quantidade * OrderItem.preco_unitario
            )
        )
        .filter(OrderItem.pedido_id == order_id)
        .scalar()
    )

    order = get_order(db, order_id)

    if order is None:
        return None

    order.total = total or 0

    db.flush()
    db.refresh(order)

    return order

def get_orders_by_user(db: Session, user_id: int):
    return (
        db.query(Order)
        .filter(Order.usuario_id == user_id)
        .all()
    )

def close_order(db: Session, order_id: int):
    order = get_order(db, order_id)

    if order is None:
        return None, "not_found"

    if order.status == "fechado":
        return None, "already_closed"

    order.status = "fechado"

    db.commit()
    db.refresh(order)

    return order, None