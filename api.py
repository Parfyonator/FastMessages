import asyncio
import os

from aioredis import create_redis_pool
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, validator
import uvicorn


class Message(BaseModel):
    value: str
    ttl: int

    @validator('ttl')
    def ttl_must_be_non_negative_int(cls, v):
        if not isinstance(v, int) or not v >= 0:
            raise ValueError('TTL must be a non-negative integer.')
        return v


app = FastAPI(debug=False)


@app.on_event('startup')
async def startup_event():
    redis_uri = os.environ.get('REDIS_URI', 'redis://127.0.0.1:6379/0?encoding=utf-8')
    app.state.redis = await create_redis_pool(redis_uri)


@app.on_event('shutdown')
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()
    

async def get_message_timeout(key: str):
    msg = await app.state.redis.get(key)
    if msg:
        return msg
        
    channels = app.state.redis.channels
    ch = channels[f'channel:{key}'.encode()]

    while (await ch.wait_message()):
        await ch.get()
        await app.state.redis.unsubscribe(f'channel:{key}')

    msg = await app.state.redis.get(key)

    return msg


@app.get('/messages/{key}')
async def get_message(key: str, timeout:int = Query(0, title='Message ID', ge=0)):
    if timeout == 0:
        msg = await app.state.redis.get(key)
        if not msg:
            raise HTTPException(status_code=404, detail="Message with given key not found.")
    
    await app.state.redis.subscribe(f'channel:{key}')
    try:
        msg = await asyncio.wait_for(get_message_timeout(key), timeout)
    except asyncio.TimeoutError:
        msg = None

    if not msg:
        raise HTTPException(status_code=404, detail="Message with given key not found.")

    return {
        "message": msg,
    }


@app.post('/messages/{key}')
async def post_message(key: str, msg: Message):
    res = await app.state.redis.execute('set', key, msg.value, 'nx', 'ex', msg.ttl)
    
    if not res:
        raise HTTPException(status_code=409, detail="Message with given key already exist.")

    await app.state.redis.publish(f'channel:{key}', 'channel message')


if __name__ == '__main__':
    uvicorn.run("api:app", host='0.0.0.0', port=8000, workers=4, reload=True)
