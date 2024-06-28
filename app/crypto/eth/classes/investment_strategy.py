from pydantic import BaseModel


class InvestmentStrategy(BaseModel):
    name: str
    key: str
    approxApy: float
