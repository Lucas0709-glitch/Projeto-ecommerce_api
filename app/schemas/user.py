from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    nome: str = Field(
        min_length=1,
        description="Nome do usuário"
    )
    email: str = Field(
        description="Endereço de e-mail do usuário"
    )
    senha: str = Field(
        description="Senha utilizada para autenticação"
    )

class UserResponse(BaseModel):
    id: int = Field(
        description="Identificador único do usuário"
    )
    nome: str = Field(
        description="Nome do usuário"
    )
    email: str = Field(
        description="Endereço de e-mail do usuário"
    )

    class Config:
        from_attributes = True
