from .swap import get_swap_data_for_chain
from .transfer import get_transfer_data_for_chain
from ..enums.evm_chain import EvmChain

SWAP = "swap"
TRANSFER = "transfer"

actions = {
    SWAP: get_swap_data_for_chain,
    TRANSFER: get_transfer_data_for_chain
}


def get_tx_data(
        action_type: str,
        params,
        config,
        evm_chain: EvmChain
    ):
    if not config:
        return False

    resolver = actions[action_type]
    return resolver(**params, evm_chain=evm_chain, method_config=config)
