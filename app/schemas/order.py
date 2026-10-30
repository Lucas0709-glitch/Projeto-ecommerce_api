from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
    criado_em: datetime = Field(
        description="Data e hora de criação do pedido"
    )