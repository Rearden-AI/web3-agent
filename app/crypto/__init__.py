from typing import Any

from . import eth, eth_holesky
from .eth_abstract.enums.evm_chain import EvmChain
from .eth_abstract.actions import get_tx_data

chains = {
    1: eth,
    17000: eth_holesky
}


def get_transaction_data(
    chain_id: int,
    data: dict[str, Any]
):
    action = data['action']
    params = data['params']
    config = chains[chain_id].available_actions[action]

    evm_chain = __get_evm_chain(chain_id)

    return {
        "network": chains[chain_id].get_network_data(),
        **get_tx_data(action, params, config, evm_chain)
    }


def __get_evm_chain(chain_id) -> EvmChain:
    if chain_id == 1:
        return EvmChain.ETH
    if chain_id == 17000:
        return EvmChain.ETH_HOLESKY
    