import datetime

from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class PromptBit(Base):
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    name: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    address: Mapped[str] = mapped_column(String(100), nullable=True)
    chain: Mapped[str] = mapped_column(String(5), nullable=False)

    def __repr__(self):
        return f"<Prompt bit [{self.id}] {self.name}>"
