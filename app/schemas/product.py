from pydantic import BaseModel


class ProductCreate(BaseModel):
    nome: str
    descricao: str
    preco: float
    estoque: int

class ProductUpdate(BaseModel):
    nome: str
    descricao: str
    preco: float
    estoque: int

class ProductResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    estoque: int

    class Config:
        from_attributes = True

