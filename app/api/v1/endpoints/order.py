from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.order import create_order
from app.schemas.order import OrderCreate, OrderResponse
from app.crud.order_item import create_order_item
from app.schemas.order_item import OrderItemCreate, OrderItemResponse
from app.crud.product import get_product
from app.crud.order import get_order, update_order_total

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
    order = get_order(db, order_item.pedido_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )
    
    product = get_product(db, order_item.produto_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )
    
    if product.estoque < order_item.quantidade:
        raise HTTPException(
            status_code=400,
            detail="Estoque insuficiente"
        )

    product.estoque -= order_item.quantidade
    db.commit()

    created_item = create_order_item(
    db,
    order_item,
    preco_unitario=product.preco
    )

    update_order_total(
        db,
        order_item.pedido_id
    )

    return created_item
