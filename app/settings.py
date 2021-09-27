import json
import os
from web3 import Web3, HTTPProvider


PANCAKESWAP_API_URL = 'https://api.pancakeswap.info/api/v2/tokens/{address}'

with open('app/pancake-pair-abi.json') as f:
    PANCAKE_PAIR_ABI = json.load(f)

w3 = Web3(HTTPProvider(os.getenv('JSON_RPC_URL')))
