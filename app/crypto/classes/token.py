from pydantic import BaseModel

from ..eth_abstract.enums.evm_chain import EvmChain


class Erc20TokenData(BaseModel):
    address: str
    decimals: int


class Token(BaseModel):
    name: str
    symbol: str
    icon_url: str
    token_data: dict[EvmChain, Erc20TokenData]
