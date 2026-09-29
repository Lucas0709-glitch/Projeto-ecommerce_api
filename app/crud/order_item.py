from sqlalchemy.orm import Session

from app.models.order_item import OrderItem
from app.schemas.order_item import OrderItemCreate


def create_order_item(
    db: Session,
    order_item: OrderItemCreate,
    preco_unitario: float
):
    db_order_item = OrderItem(
        pedido_id=order_item.pedido_id,
        produto_id=order_item.produto_id,
        quantidade=order_item.quantidade,
        preco_unitario=preco_unitario
    )

    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)

    return db_order_item