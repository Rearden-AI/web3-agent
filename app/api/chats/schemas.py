import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.core.models.base import State


class ChatBase(BaseModel):
    name: str | None = None
    uuid: str


class ChatCreate(ChatBase):
    pass


class ChatUpdate(ChatBase):
    pass


class ChatUpdatePartial(ChatBase):
    name: str | None = None
    uuid: None = None


class ChatSchema(ChatBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime
    state: State
    user_id: int


class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    exec_logs: str | None = None
    body: str
    transactions: list | None = None
    timestamp: int
    chooseable_actions: list | None = None
    actions: list | None = None


class StrategyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ExtendedChatSchema(ChatSchema):
    model_config = ConfigDict(from_attributes=True)

    history: list = []


class DataIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    context_data: dict | None = None
    message: str
    chain_id: int
    generate_code: list | None = None
    transaction_ids: list[int] | None = None
    chosen_action_key: str | None = None
    timestamp: int