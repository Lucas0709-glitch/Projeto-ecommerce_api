from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, utcnow


class OrderStatus(StrEnum):
    ABERTO = "aberto"
    FECHADO = "fechado"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    total: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow
    )

    usuario = relationship("User", back_populates="pedidos")
    itens = relationship("OrderItem", back_populates="pedido")