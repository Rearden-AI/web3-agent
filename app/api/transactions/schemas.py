from enum import Enum

from pydantic import BaseModel, ConfigDict


class TransactionStatus(str, Enum):
    pending = "pending"
    succeeded = "succeeded"
    failed = "failed"
    waiting = "waiting"


class TransactionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    amount: str
    token_symbol: str
    transaction_type: str
    status: TransactionStatus
    transaction_hash: str | None = None
    to_address: str
    from_address: str
    chat_uuid: str
    action_name: str
    network: str
    timestamp: int


class TransactionSchema(TransactionBase):
    pass


class TransactionCreate(TransactionBase):
    user_id: int | None = None


class TransactionExtended(TransactionBase):
    id: int


class TransactionUpdate(BaseModel):
    transaction_hash: str | None = None
    status: TransactionStatus | None = None
