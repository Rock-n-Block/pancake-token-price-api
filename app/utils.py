import requests
from app.settings import w3, PANCAKESWAP_API_URL, PANCAKE_PAIR_ABI
from web3 import Web3
from math import sqrt


def calculate_lp_token_price(address):
    address_checksum = Web3.toChecksumAddress(address)
    contract = w3.eth.contract(address=address_checksum, abi=PANCAKE_PAIR_ABI)
    total_supply = contract.functions.totalSupply().call()
    reserve0, reserve1, _ = contract.functions.getReserves().call()
    token0 = contract.functions.token0().call()
    token1 = contract.functions.token1().call()
    token0_info = requests.get(PANCAKESWAP_API_URL.format(address=token0)).json()['data']
    token1_info = requests.get(PANCAKESWAP_API_URL.format(address=token1)).json()['data']
    token0_price = float(token0_info['price'])
    token1_price = float(token1_info['price'])
    price = 2 * sqrt(reserve0 * reserve1) * sqrt(token0_price * token1_price) / total_supply
    return price
