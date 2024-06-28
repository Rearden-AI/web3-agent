from ...eth_abstract.actions.swap.configs.swap_config import SwapConfig

WETH_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
UNISWAP_ROUTER_ADDRESS = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"


swap_config = SwapConfig(
    weth_address=WETH_ADDRESS,
    uniswap_v2_router_address=UNISWAP_ROUTER_ADDRESS,
    application_data={
        "name": "Uniswap",
        "url": "https://app.uniswap.org/",
        "contract_address": UNISWAP_ROUTER_ADDRESS,
        "contract_address_on_explorer": 
            f"https://etherscan.io/address/{UNISWAP_ROUTER_ADDRESS}"
    }
)
