from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    nome: str = Field(
    min_length=1,
    description="Nome do produto"
    )
    descricao: str = Field(
    min_length=1,
    description="Descrição detalhada do produto"
    )
    preco: float = Field(
    ge=0,
    description="Preço do produto"
    )
    estoque: int = Field(
    ge=0,
    description="Quantidade disponível em estoque"
    )

class ProductUpdate(BaseModel):
    nome: str = Field(
    min_length=1,
    description="Nome do produto"
    )
    descricao: str = Field(
    min_length=1,
    description="Descrição detalhada do produto"
    )
    preco: float = Field(
    ge=0,
    description="Preço do produto"
    )
    estoque: int = Field(
    ge=0,
    description="Quantidade disponível em estoque"
    )

class ProductResponse(BaseModel):
    id: int = Field(
        description="Identificador único do produto"
    )
    nome: str = Field(
        description="Nome do produto"
    )
    descricao: str = Field(
        description="Descrição detalhada do produto"
    )
    preco: float = Field(
        description="Preço do produto"
    )
    estoque: int = Field(
        description="Quantidade disponível em estoque"
    )

    class Config:
        from_attributes = True

