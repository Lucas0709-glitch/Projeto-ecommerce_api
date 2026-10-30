from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    nome: str = Field(
        min_length=1,
        max_length=100,
        description="Nome do usuário"
    )
    email: EmailStr = Field(
        description="Endereço de e-mail do usuário"
    )
    senha: str = Field(
        min_length=8,
        max_length=128,
        description="Senha utilizada para autenticação (mínimo de 8 caracteres)"
    )

    @field_validator("email")
    @classmethod
    def normalizar_email(cls, valor: str) -> str:
        return valor.lower()


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        description="Identificador único do usuário"
    )
    nome: str = Field(
        description="Nome do usuário"
    )
    email: str = Field(
        description="Endereço de e-mail do usuário"
    )
    criado_em: datetime = Field(
        description="Data e hora de criação do usuário"
    )