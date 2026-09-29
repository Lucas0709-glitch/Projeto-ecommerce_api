from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    pedido_id: int = Field(
        description="Identificador do pedido"
    )
    produto_id: int = Field(
        description="Identificador do produto"
    )
    quantidade: int = Field(
        description="Quantidade do produto no pedido"
    )


class OrderItemResponse(BaseModel):
    id: int = Field(
        description="Identificador único do item do pedido"
    )
    pedido_id: int = Field(
        description="Identificador do pedido"
    )
    produto_id: int = Field(
        description="Identificador do produto"
    )
    quantidade: int = Field(
        description="Quantidade do produto no pedido"
    )
    preco_unitario: float = Field(
        description="Preço do produto no momento da compra"
    )

    class Config:
        from_attributes = True