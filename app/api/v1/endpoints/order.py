from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.models.order import OrderStatus

from app.schemas.order import OrderResponse
from app.schemas.order_item import OrderItemCreate, OrderItemResponse

from app.crud.order_item import create_order_item, get_order_items
from app.crud.product import get_product
from app.crud.order import (
    close_order,
    create_order,
    get_order,
    get_orders_by_user,
    update_order_total
)

router = APIRouter(
    tags=["Pedidos"]
)


def get_own_order_or_404(db: Session, order_id: int, current_user: User):
    """Busca o pedido e garante que ele pertence ao usuário logado."""
    order = get_order(db, order_id)

    if order is None or order.usuario_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    return order


@router.post(
    "/orders",
    response_model=OrderResponse,
    status_code=201,
    summary="Cadastrar pedido",
    description="Cria um novo pedido para o usuário autenticado."
)
def register_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_order(db, current_user.id)


@router.get(
    "/orders",
    response_model=list[OrderResponse],
    summary="Listar meus pedidos",
    description="Retorna todos os pedidos do usuário autenticado."
)
def list_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_orders_by_user(db, current_user.id)


@router.post(
    "/orders/items",
    response_model=OrderItemResponse,
    status_code=201,
    summary="Adicionar item ao pedido",
    description="Adiciona um produto a um pedido do usuário autenticado."
)
def register_order_item(
    order_item: OrderItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = get_own_order_or_404(db, order_item.pedido_id, current_user)

    if order.status == OrderStatus.FECHADO:
        raise HTTPException(
            status_code=400,
            detail="Não é possível adicionar itens a um pedido fechado"
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

    created_item = create_order_item(
        db,
        order_item,
        preco_unitario=product.preco
    )

    update_order_total(db, order_item.pedido_id)

    db.commit()

    return created_item


@router.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
    summary="Buscar pedido",
    description="Retorna um pedido do usuário autenticado pelo seu ID."
)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_own_order_or_404(db, order_id, current_user)


@router.get(
    "/orders/{order_id}/items",
    response_model=list[OrderItemResponse],
    summary="Listar itens do pedido",
    description="Retorna os itens de um pedido do usuário autenticado."
)
def list_order_items(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_own_order_or_404(db, order_id, current_user)

    return get_order_items(db, order_id)


@router.put(
    "/orders/{order_id}/close",
    response_model=OrderResponse,
    summary="Fechar pedido",
    description="Altera o status de um pedido aberto para fechado.",
    responses={404: {"description": "Pedido não encontrado"}}
)
def close_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_own_order_or_404(db, order_id, current_user)

    order, error = close_order(db, order_id)

    if error == "not_found":
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    if error == "already_closed":
        raise HTTPException(
            status_code=400,
            detail="Pedido já está fechado"
        )

    return order