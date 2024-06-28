import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import func, String, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base

if TYPE_CHECKING:
    from .user import User


class TransactionStatus(Enum):
    pending = "pending"
    succeeded = "succeeded"
    failed = "failed"
    waiting = "waiting"


class Transaction(Base):
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), nullable=False)

    amount: Mapped[str] = mapped_column(String(128), nullable=False)
    token_symbol: Mapped[str] = mapped_column(String(10), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(server_default=TransactionStatus.waiting.value, nullable=False)
    transaction_hash: Mapped[str] = mapped_column(String(128), nullable=True, unique=True)
    to_address: Mapped[str] = mapped_column(String(128), nullable=True)
    from_address: Mapped[str] = mapped_column(String(128), nullable=True)
    chat_uuid: Mapped[str] = mapped_column(String(36), nullable=False)
    action_name: Mapped[str] = mapped_column(String(36), nullable=False)
    network: Mapped[str] = mapped_column(String(36), nullable=False)
    timestamp: Mapped[int] = mapped_column(BigInteger, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
