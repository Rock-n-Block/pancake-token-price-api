import requests
import aioredis
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from app.settings import PANCAKESWAP_API_URL
from app.utils import calculate_lp_token_price


class Payload(BaseModel):
    addresses: List[str]


class Response(BaseModel):
    prices: Dict[str, float]


app = FastAPI()


@app.post('/', response_model=Response)
async def prices(payload: Payload):
    redis = await aioredis.from_url("redis://redis:6379", encoding="utf-8", decode_responses=True)
    result = {}
    for address in payload.addresses:
        price = await redis.get(address)
        if not price:
            response = requests.get(PANCAKESWAP_API_URL.format(address=address)).json()
            symbol = response['data']['symbol']
            if symbol != 'Cake-LP':
                price = response['data']['price']
            else:
                price = calculate_lp_token_price(address)

            await redis.set(address, price, ex=60)

        result[address] = price

    return {'prices': result}
