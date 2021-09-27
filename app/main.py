import requests
import aioredis
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app.settings import PANCAKESWAP_API_URL
from app.utils import calculate_lp_token_price


class Payload(BaseModel):
    addresses: List[str]


app = FastAPI()


@app.post('/')
async def main(payload: Payload):
    redis = await aioredis.from_url("redis://redis:6379", encoding="utf-8", decode_responses=True)
    result = {}
    for address in payload.addresses:
        price = await redis.get(address)
        if not price:
            print('write')
            response = requests.get(PANCAKESWAP_API_URL.format(address=address)).json()
            symbol = response['data']['symbol']
            if symbol != 'Cake-LP':
                price = response['data']['price']
            else:
                price = calculate_lp_token_price(address)

            await redis.set(address, price, ex=60)
        else:
            print('cache')

        result[address] = price

    return result
