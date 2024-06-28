from ..constants.links import ETH_ICON_URL


def get_network_data():
    return {
        "name": "Mainnet",
        "icon": ETH_ICON_URL,
        "chain": {
            "type": "evm",
            "chainId": 1
        }
    }
