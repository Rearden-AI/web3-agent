from ...eth_abstract.enums.contract_type import ContractType

contracts = {
    ContractType.STETH: "0x3F1c547b21f65e10480dE3ad8E19fAAC46C95034",
    ContractType.EIGENLAYER_STRATEGY_MANAGER: "0xdfB5f6CE42aAA7830E94ECFCcAd411beF4d4D5b6",
    ContractType.STETH_EIGENLAYER_STRATEGY: "0x7D704507b76571a51d9caE8AdDAbBFd0ba0e63d3"
}

def get_contract_address(
        contract: ContractType
):
    return contracts[contract]
