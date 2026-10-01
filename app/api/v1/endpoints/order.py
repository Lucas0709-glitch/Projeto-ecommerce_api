from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db

from app.schemas.order import OrderCreate, OrderResponse
from app.schemas.order_item import OrderItemCreate, OrderItemResponse

from app.crud.user import get_user
from app.crud.order_item import create_order_item, get_order_items
from app.crud.product import get_product
from app.crud.order import (
    create_order,
    get_order,
    get_orders_by_user,
    update_order_total
)

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


@router.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
    summary="Buscar pedido",
    description="Retorna um pedido específico pelo seu ID."
)
def read_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = get_order(db, order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    return order


@router.get(
    "/orders/{order_id}/items",
    response_model=list[OrderItemResponse],
    summary="Listar itens do pedido",
    description="Retorna todos os itens pertencentes a um pedido."
)
def list_order_items(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = get_order(db, order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    return get_order_items(db, order_id)


@router.get(
    "/users/{user_id}/orders",
    response_model=list[OrderResponse],
    summary="Listar pedidos do usuário",
    description="Retorna todos os pedidos realizados por um usuário."
)
def list_user_orders(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return get_orders_by_user(db, user_id)


