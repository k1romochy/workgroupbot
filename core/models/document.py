from datetime import datetime

from sqlalchemy import func, BigInteger

from core.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Document(Base):
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now
    )
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    url: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
