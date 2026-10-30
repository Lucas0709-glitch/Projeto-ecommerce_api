from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.product import (
    create_product,
    delete_product,
    get_product,
    get_products,
    product_has_orders,
    update_product
)
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(
    tags=["Produtos"]
)

@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=201,
    summary="Cadastrar produto",
    description="Cadastra um novo produto no catálogo.",
    responses={
        201: {
            "description": "Produto criado com sucesso"
        }
    }
)
def register_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_product(db, product)



@router.get(
    "/products",
    response_model=list[ProductResponse],
    summary="Listar produtos",
    description="Retorna todos os produtos cadastrados no catálogo."
)
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_products(db)



@router.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    summary="Buscar produto",
    description="Retorna um produto específico pelo seu ID.",
    responses={
        404: {
            "description": "Produto não encontrado"
        }
    }
)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = get_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return product



@router.put(
    "/products/{product_id}",
    response_model=ProductResponse,
    summary="Atualizar produto",
    description="Atualiza os dados de um produto existente pelo seu ID.",
    responses={
        404: {
            "description": "Produto não encontrado"
        }
    }
)
def update_product_endpoint(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = update_product(db, product_id, product_data)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return product



@router.delete(
    "/products/{product_id}",
    response_model=ProductResponse,
    summary="Excluir produto",
    description="Exclui um produto existente pelo seu ID.",
    responses={
        409: {
            "description": "Produto já está em pedidos"
        }
    }
)
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = get_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    if product_has_orders(db, product_id):
        raise HTTPException(
            status_code=409,
            detail="Produto já foi vendido e não pode ser excluído"
        )

    return delete_product(db, product_id)