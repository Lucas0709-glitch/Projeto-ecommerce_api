from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.user import create_user
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user)