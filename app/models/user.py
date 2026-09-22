from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    nome: Mapped[str] = mapped_column(String(100))

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True
    )

    senha_hash: Mapped[str] = mapped_column(String(255))

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )