import pickle
import json
import requests

from app.core.modules_factory import redis_db
from ..classes import Token, Erc20TokenData
from ..eth_abstract.enums.evm_chain import EvmChain

CACHE_TOKENS_KEY = 'erc-20-tokens-new-2'


def get_tokens() -> list[Token]:
    tokens = __get_erc_20_tokens_from_cache()

    if not tokens:
        tokens = __get_erc_20_tokens_from_api()
        redis_db.set(CACHE_TOKENS_KEY, pickle.dumps(tokens))

    return tokens


def get_token_by_symbol(symbol: str) -> Token:
    return next(x for x in get_tokens() if x.symbol == symbol)


def __get_erc_20_tokens_from_cache() -> list[Token]:
    try:
        if data := redis_db.get(CACHE_TOKENS_KEY):
            return pickle.loads(data)
    except:
        pass
    
    return None



def __get_erc_20_tokens_from_api() -> list[Token]:
    url = 'https://api.coinranking.com/v2/coins'
    response = requests.get(url)

    result = json.loads(response.text)
    coins = result['data']['coins']

    filter_erc = lambda coin: any(address.startswith('ethereum/') for address in coin['contractAddresses'])
    map_to_eth_address = lambda coin: next((addr.split('/')[1] for addr in coin['contractAddresses'] if addr.startswith('ethereum/')), None)
    get_eth_token_data = lambda coin: {
        EvmChain.ETH: Erc20TokenData(
            address=map_to_eth_address(coin),
            decimals=__get_decimals(map_to_eth_address(coin)),
        )
    }
    map_to_token = lambda coin: Token(
        name=coin['name'],
        symbol=coin['symbol'],
        icon_url=coin.get('iconUrl'),
        token_data=get_eth_token_data(coin)
    )

    tokens = list(map(map_to_token, filter(filter_erc, coins)))
    for token in tokens:
        if token.symbol == 'USDT':
            token.token_data[EvmChain.ETH_HOLESKY] = Erc20TokenData(
                decimals=18,
                address='0xEF388C3bd1E5Fb06012de192e637c8dd54F3933b'
            )

        if token.symbol == 'DAI':
            token.token_data[EvmChain.ETH_HOLESKY] = Erc20TokenData(
                address='0x86Db6AD79793434627293c0B7801be04Aa783030',
                decimals=18
            )

    print(tokens)

    return tokens


def __get_decimals(token_address: str) -> int:
    if token_address.casefold() == '0xdac17f958d2ee523a2206206994597c13d831ec7'.casefold():
        return 6

    if token_address.casefold() == '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'.casefold():
        return 6

    if token_address.casefold() == '0x582d872a1b094fc48f5de31d3b73f2d9be47def1'.casefold():
        return 9

    if token_address.casefold() == '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599'.casefold():
        return 8

    if token_address.casefold() == '0x85f17cf997934a597031b2e18a9ab6ebd4b9f6a4'.casefold():
        return 24

    if token_address.casefold() == '0x8D983cb9388EaC77af0474fA441C4815500Cb7BB'.casefold():
        return 6

    return 18
