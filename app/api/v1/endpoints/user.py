from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.user import create_user
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(
    tags=["Usuários"]
)

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    summary="Cadastrar usuário",
    description="Cadastra um novo usuário no sistema.",
    responses={
        201: {
            "description": "Usuário criado com sucesso"
        }
    }
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user)