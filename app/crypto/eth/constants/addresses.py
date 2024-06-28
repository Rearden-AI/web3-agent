from ...eth_abstract.enums.contract_type import ContractType

contracts = {
    ContractType.STETH: "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
    ContractType.EIGENLAYER_STRATEGY_MANAGER: "0x858646372CC42E1A627fcE94aa7A7033e7CF075A",
    ContractType.STETH_EIGENLAYER_STRATEGY: "0x93c4b944D05dfe6df7645A86cd2206016c51564D"
}

def get_contract_address(
        contract: ContractType
):
    return contracts[contract]
