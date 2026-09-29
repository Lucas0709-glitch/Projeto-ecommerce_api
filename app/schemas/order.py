from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    usuario_id: int = Field(
        description="Identificador do usuário que está realizando o pedido"
    )


class OrderResponse(BaseModel):
    id: int = Field(
        description="Identificador único do pedido"
    )
    usuario_id: int = Field(
        description="Identificador do usuário responsável pelo pedido"
    )
    status: str = Field(
        description="Status atual do pedido"
    )
    total: float = Field(
        description="Valor total do pedido"
    )

    class Config:
        from_attributes = True