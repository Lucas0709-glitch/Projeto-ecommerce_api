from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    nome: str = Field(
        description="Nome do usuário"
    )
    email: str = Field(
        description="Endereço de e-mail do usuário"
    )
    senha: str = Field(
        description="Senha utilizada para autenticação"
    )

class UserResponse(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True
