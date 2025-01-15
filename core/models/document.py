from sqlalchemy import BigInteger

from core.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Document(Base):
    term: Mapped[int] = mapped_column(unique=False, nullable=False)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    url: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    registrated_at: Mapped[str] = mapped_column(nullable=False)
