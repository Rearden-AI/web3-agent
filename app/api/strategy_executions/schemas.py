from pydantic import BaseModel, ConfigDict


class StrategyExecutionBase(BaseModel):
    chat_uuid: str
    # user_id: int


class StrategyExecutionCreate(StrategyExecutionBase):
    pass


class StrategyExecution(StrategyExecutionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
