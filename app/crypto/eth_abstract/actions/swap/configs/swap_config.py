from pydantic import BaseModel


class SwapConfig(BaseModel):
    weth_address: str
    uniswap_v2_router_address: str
    application_data: dict[str, str]
