from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.product import (
    create_product,
    delete_product,
    get_product,
    get_products,
    update_product
)
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter()


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
    db: Session = Depends(get_db)
):
    return create_product(db, product)



@router.get(
    "/products",
    response_model=list[ProductResponse],
    summary="Listar produtos",
    description="Retorna todos os produtos cadastrados no catálogo."
)
def list_products(
    db: Session = Depends(get_db)
):
    return get_products(db)



@router.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    summary="Buscar produto",
    description="Retorna um produto específico pelo seu ID."
)
def read_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return get_product(db, product_id)



@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product_endpoint(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    return update_product(db, product_id, product_data)



@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db)
):
    return delete_product(db, product_id)