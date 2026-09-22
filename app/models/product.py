from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    nome: Mapped[str] = mapped_column(String(150))

    descricao: Mapped[str] = mapped_column(Text)

    preco: Mapped[float] = mapped_column(Numeric(10, 2))

    estoque: Mapped[int] = mapped_column(Integer)

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )