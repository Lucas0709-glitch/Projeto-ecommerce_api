from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user: UserCreate):
    db_user = User(
        nome=user.nome,
        email=user.email,
        senha_hash=user.senha
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user