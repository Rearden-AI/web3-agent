from ...eth_abstract.actions.swap.configs.swap_config import SwapConfig

WETH_ADDRESS = "0x35060f7803eF7763b77E4EF0082bc0bCf2654154"
DONASWAP_ROUTER_ADDRESS = "0x6E682B51F8bb67294B522b75a1E79dDd4502cc94"


swap_config = SwapConfig(
    weth_address=WETH_ADDRESS,
    uniswap_v2_router_address=DONASWAP_ROUTER_ADDRESS,
    application_data={
        "name": "DonaSwap",
        "url": "https://donaswap.io/",
        "contract_address": DONASWAP_ROUTER_ADDRESS,
        "contract_address_on_explorer": 
            f"https://holesky.etherscan.io/address/{DONASWAP_ROUTER_ADDRESS}"
    }
)
