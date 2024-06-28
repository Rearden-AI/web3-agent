# pylint: disable=missing-module-docstring, missing-function-docstring, relative-beyond-top-level, line-too-long
from ..enums.contract_type import ContractType


abis = {
    ContractType.STETH: '[{"constant":false,"inputs":[],"name":"resume","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[],"name":"stop","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"hasInitialized","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_amount","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"STAKING_CONTROL_ROLE","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_ethAmount","type":"uint256"}],"name":"getSharesByPooledEth","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"isStakingPaused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_sender","type":"address"},{"name":"_recipient","type":"address"},{"name":"_amount","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_script","type":"bytes"}],"name":"getEVMScriptExecutor","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_maxStakeLimit","type":"uint256"},{"name":"_stakeLimitIncreasePerBlock","type":"uint256"}],"name":"setStakingLimit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"RESUME_ROLE","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_lidoLocator","type":"address"},{"name":"_eip712StETH","type":"address"}],"name":"finalizeUpgrade_v2","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"getRecoveryVault","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTotalPooledEther","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_newDepositedValidators","type":"uint256"}],"name":"unsafeChangeDepositedValidators","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"PAUSE_ROLE","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getTreasury","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"isStopped","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getBufferedEther","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_lidoLocator","type":"address"},{"name":"_eip712StETH","type":"address"}],"name":"initialize","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[],"name":"receiveELRewards","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getWithdrawalCredentials","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getCurrentStakeLimit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getStakeLimitFullInfo","outputs":[{"name":"isStakingPaused","type":"bool"},{"name":"isStakingLimitSet","type":"bool"},{"name":"currentStakeLimit","type":"uint256"},{"name":"maxStakeLimit","type":"uint256"},{"name":"maxStakeLimitGrowthBlocks","type":"uint256"},{"name":"prevStakeLimit","type":"uint256"},{"name":"prevStakeBlockNumber","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_sender","type":"address"},{"name":"_recipient","type":"address"},{"name":"_sharesAmount","type":"uint256"}],"name":"transferSharesFrom","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"resumeStaking","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getFeeDistribution","outputs":[{"name":"treasuryFeeBasisPoints","type":"uint16"},{"name":"insuranceFeeBasisPoints","type":"uint16"},{"name":"operatorsFeeBasisPoints","type":"uint16"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"receiveWithdrawals","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"_sharesAmount","type":"uint256"}],"name":"getPooledEthByShares","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"token","type":"address"}],"name":"allowRecoverability","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"owner","type":"address"}],"name":"nonces","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"appId","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getOracle","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"eip712Domain","outputs":[{"name":"name","type":"string"},{"name":"version","type":"string"},{"name":"chainId","type":"uint256"},{"name":"verifyingContract","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getContractVersion","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getInitializationBlock","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_recipient","type":"address"},{"name":"_sharesAmount","type":"uint256"}],"name":"transferShares","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"getEIP712StETH","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"","type":"address"}],"name":"transferToVault","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_sender","type":"address"},{"name":"_role","type":"bytes32"},{"name":"_params","type":"uint256[]"}],"name":"canPerform","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_referral","type":"address"}],"name":"submit","outputs":[{"name":"","type":"uint256"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getEVMScriptRegistry","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_recipient","type":"address"},{"name":"_amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_maxDepositsCount","type":"uint256"},{"name":"_stakingModuleId","type":"uint256"},{"name":"_depositCalldata","type":"bytes"}],"name":"deposit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"UNSAFE_CHANGE_DEPOSITED_VALIDATORS_ROLE","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getBeaconStat","outputs":[{"name":"depositedValidators","type":"uint256"},{"name":"beaconValidators","type":"uint256"},{"name":"beaconBalance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"removeStakingLimit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_reportTimestamp","type":"uint256"},{"name":"_timeElapsed","type":"uint256"},{"name":"_clValidators","type":"uint256"},{"name":"_clBalance","type":"uint256"},{"name":"_withdrawalVaultBalance","type":"uint256"},{"name":"_elRewardsVaultBalance","type":"uint256"},{"name":"_sharesRequestedToBurn","type":"uint256"},{"name":"_withdrawalFinalizationBatches","type":"uint256[]"},{"name":"_simulatedShareRate","type":"uint256"}],"name":"handleOracleReport","outputs":[{"name":"postRebaseAmounts","type":"uint256[4]"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getFee","outputs":[{"name":"totalFee","type":"uint16"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"kernel","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTotalShares","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"},{"name":"_deadline","type":"uint256"},{"name":"_v","type":"uint8"},{"name":"_r","type":"bytes32"},{"name":"_s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"isPetrified","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getLidoLocator","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"canDeposit","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"STAKING_PAUSE_ROLE","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getDepositableEther","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_account","type":"address"}],"name":"sharesOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"pauseStaking","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getTotalELRewardsCollected","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[],"name":"StakingPaused","type":"event"},{"anonymous":false,"inputs":[],"name":"StakingResumed","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"maxStakeLimit","type":"uint256"},{"indexed":false,"name":"stakeLimitIncreasePerBlock","type":"uint256"}],"name":"StakingLimitSet","type":"event"},{"anonymous":false,"inputs":[],"name":"StakingLimitRemoved","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"reportTimestamp","type":"uint256"},{"indexed":false,"name":"preCLValidators","type":"uint256"},{"indexed":false,"name":"postCLValidators","type":"uint256"}],"name":"CLValidatorsUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"depositedValidators","type":"uint256"}],"name":"DepositedValidatorsChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"reportTimestamp","type":"uint256"},{"indexed":false,"name":"preCLBalance","type":"uint256"},{"indexed":false,"name":"postCLBalance","type":"uint256"},{"indexed":false,"name":"withdrawalsWithdrawn","type":"uint256"},{"indexed":false,"name":"executionLayerRewardsWithdrawn","type":"uint256"},{"indexed":false,"name":"postBufferedEther","type":"uint256"}],"name":"ETHDistributed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"reportTimestamp","type":"uint256"},{"indexed":false,"name":"timeElapsed","type":"uint256"},{"indexed":false,"name":"preTotalShares","type":"uint256"},{"indexed":false,"name":"preTotalEther","type":"uint256"},{"indexed":false,"name":"postTotalShares","type":"uint256"},{"indexed":false,"name":"postTotalEther","type":"uint256"},{"indexed":false,"name":"sharesMintedAsFees","type":"uint256"}],"name":"TokenRebased","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"lidoLocator","type":"address"}],"name":"LidoLocatorSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"ELRewardsReceived","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"WithdrawalsReceived","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"},{"indexed":false,"name":"amount","type":"uint256"},{"indexed":false,"name":"referral","type":"address"}],"name":"Submitted","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Unbuffered","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"executor","type":"address"},{"indexed":false,"name":"script","type":"bytes"},{"indexed":false,"name":"input","type":"bytes"},{"indexed":false,"name":"returnData","type":"bytes"}],"name":"ScriptResult","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"vault","type":"address"},{"indexed":true,"name":"token","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"RecoverToVault","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"eip712StETH","type":"address"}],"name":"EIP712StETHInitialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"sharesValue","type":"uint256"}],"name":"TransferShares","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"account","type":"address"},{"indexed":false,"name":"preRebaseTokenAmount","type":"uint256"},{"indexed":false,"name":"postRebaseTokenAmount","type":"uint256"},{"indexed":false,"name":"sharesAmount","type":"uint256"}],"name":"SharesBurnt","type":"event"},{"anonymous":false,"inputs":[],"name":"Stopped","type":"event"},{"anonymous":false,"inputs":[],"name":"Resumed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"version","type":"uint256"}],"name":"ContractVersionSet","type":"event"}]',
    ContractType.EIGENLAYER_STRATEGY_MANAGER: '[{"inputs":[{"internalType":"contract IDelegationManager","name":"_delegation","type":"address"},{"internalType":"contract IEigenPodManager","name":"_eigenPodManager","type":"address"},{"internalType":"contract ISlasher","name":"_slasher","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"staker","type":"address"},{"indexed":false,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":false,"internalType":"contract IStrategy","name":"strategy","type":"address"},{"indexed":false,"internalType":"uint256","name":"shares","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":false,"internalType":"uint256","name":"newPausedStatus","type":"uint256"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"contract IPauserRegistry","name":"pauserRegistry","type":"address"},{"indexed":false,"internalType":"contract IPauserRegistry","name":"newPauserRegistry","type":"address"}],"name":"PauserRegistrySet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"contract IStrategy","name":"strategy","type":"address"}],"name":"StrategyAddedToDepositWhitelist","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"contract IStrategy","name":"strategy","type":"address"}],"name":"StrategyRemovedFromDepositWhitelist","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAddress","type":"address"},{"indexed":false,"internalType":"address","name":"newAddress","type":"address"}],"name":"StrategyWhitelisterChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":false,"internalType":"uint256","name":"newPausedStatus","type":"uint256"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"contract IStrategy","name":"strategy","type":"address"},{"indexed":false,"internalType":"bool","name":"value","type":"bool"}],"name":"UpdatedThirdPartyTransfersForbidden","type":"event"},{"inputs":[],"name":"DEPOSIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DOMAIN_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"contract IStrategy","name":"strategy","type":"address"},{"internalType":"uint256","name":"shares","type":"uint256"}],"name":"addShares","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IStrategy[]","name":"strategiesToWhitelist","type":"address[]"},{"internalType":"bool[]","name":"thirdPartyTransfersForbiddenValues","type":"bool[]"}],"name":"addStrategiesToDepositWhitelist","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"contract IStrategy[]","name":"strategies","type":"address[]"},{"internalType":"uint256[]","name":"shares","type":"uint256[]"},{"internalType":"address","name":"staker","type":"address"},{"components":[{"internalType":"address","name":"withdrawer","type":"address"},{"internalType":"uint96","name":"nonce","type":"uint96"}],"internalType":"struct IStrategyManager.DeprecatedStruct_WithdrawerAndNonce","name":"withdrawerAndNonce","type":"tuple"},{"internalType":"uint32","name":"withdrawalStartBlock","type":"uint32"},{"internalType":"address","name":"delegatedAddress","type":"address"}],"internalType":"struct IStrategyManager.DeprecatedStruct_QueuedWithdrawal","name":"queuedWithdrawal","type":"tuple"}],"name":"calculateWithdrawalRoot","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"delegation","outputs":[{"internalType":"contract IDelegationManager","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IStrategy","name":"strategy","type":"address"},{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"depositIntoStrategy","outputs":[{"internalType":"uint256","name":"shares","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IStrategy","name":"strategy","type":"address"},{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"staker","type":"address"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"name":"depositIntoStrategyWithSignature","outputs":[{"internalType":"uint256","name":"shares","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"domainSeparator","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"eigenPodManager","outputs":[{"internalType":"contract IEigenPodManager","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"staker","type":"address"}],"name":"getDeposits","outputs":[{"internalType":"contract IStrategy[]","name":"","type":"address[]"},{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"initialOwner","type":"address"},{"internalType":"address","name":"initialStrategyWhitelister","type":"address"},{"internalType":"contract IPauserRegistry","name":"_pauserRegistry","type":"address"},{"internalType":"uint256","name":"initialPausedStatus","type":"uint256"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"contract IStrategy[]","name":"strategies","type":"address[]"},{"internalType":"uint256[]","name":"shares","type":"uint256[]"},{"internalType":"address","name":"staker","type":"address"},{"components":[{"internalType":"address","name":"withdrawer","type":"address"},{"internalType":"uint96","name":"nonce","type":"uint96"}],"internalType":"struct IStrategyManager.DeprecatedStruct_WithdrawerAndNonce","name":"withdrawerAndNonce","type":"tuple"},{"internalType":"uint32","name":"withdrawalStartBlock","type":"uint32"},{"internalType":"address","name":"delegatedAddress","type":"address"}],"internalType":"struct IStrategyManager.DeprecatedStruct_QueuedWithdrawal","name":"queuedWithdrawal","type":"tuple"}],"name":"migrateQueuedWithdrawal","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"newPausedStatus","type":"uint256"}],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"pauseAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint8","name":"index","type":"uint8"}],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pauserRegistry","outputs":[{"internalType":"contract IPauserRegistry","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"contract IStrategy","name":"strategy","type":"address"},{"internalType":"uint256","name":"shares","type":"uint256"}],"name":"removeShares","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IStrategy[]","name":"strategiesToRemoveFromWhitelist","type":"address[]"}],"name":"removeStrategiesFromDepositWhitelist","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IPauserRegistry","name":"newPauserRegistry","type":"address"}],"name":"setPauserRegistry","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newStrategyWhitelister","type":"address"}],"name":"setStrategyWhitelister","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IStrategy","name":"strategy","type":"address"},{"internalType":"bool","name":"value","type":"bool"}],"name":"setThirdPartyTransfersForbidden","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"slasher","outputs":[{"internalType":"contract ISlasher","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"stakerStrategyList","outputs":[{"internalType":"contract IStrategy","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"staker","type":"address"}],"name":"stakerStrategyListLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"contract IStrategy","name":"","type":"address"}],"name":"stakerStrategyShares","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IStrategy","name":"","type":"address"}],"name":"strategyIsWhitelistedForDeposit","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"strategyWhitelister","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IStrategy","name":"","type":"address"}],"name":"thirdPartyTransfersForbidden","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newPausedStatus","type":"uint256"}],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"contract IStrategy","name":"strategy","type":"address"},{"internalType":"uint256","name":"shares","type":"uint256"},{"internalType":"contract IERC20","name":"token","type":"address"}],"name":"withdrawSharesAsTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"withdrawalRootPending","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]',
}


def get_abi(contract: ContractType):
    return abis[contract]
