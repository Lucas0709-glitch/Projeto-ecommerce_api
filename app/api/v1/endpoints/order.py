from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.order import create_order
from app.schemas.order import OrderCreate, OrderResponse
from app.crud.order_item import create_order_item
from app.schemas.order_item import OrderItemCreate, OrderItemResponse

router = APIRouter(
    tags=["Pedidos"]
)


@router.post(
    "/orders",
    response_model=OrderResponse,
    status_code=201,
    summary="Cadastrar pedido",
    description="Cria um novo pedido para um usuário."
)
def register_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    return create_order(db, order)

@router.post(
    "/orders/items",
    response_model=OrderItemResponse,
    status_code=201,
    summary="Adicionar item ao pedido",
    description="Adiciona um produto a um pedido existente."
)
def register_order_item(
    order_item: OrderItemCreate,
    db: Session = Depends(get_db)
):
    return create_order_item(
        db,
        order_item,
        preco_unitario=0
    )