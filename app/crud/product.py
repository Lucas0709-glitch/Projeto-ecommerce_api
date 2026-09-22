from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        nome=product.nome,
        descricao=product.descricao,
        preco=product.preco,
        estoque=product.estoque
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

def get_products(db: Session):
    return db.query(Product).all()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    db_product = get_product(db, product_id)

    if db_product is None:
        return None

    db_product.nome = product_data.nome
    db_product.descricao = product_data.descricao
    db_product.preco = product_data.preco
    db_product.estoque = product_data.estoque

    db.commit()
    db.refresh(db_product)

    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)

    if db_product is None:
        return None

    db.delete(db_product)
    db.commit()

    return db_product