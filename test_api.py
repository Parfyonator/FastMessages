import asyncio

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from api import app


@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client, LifespanManager(app):
        await app.state.redis.execute('del', '1')
        await app.state.redis.execute('del', '2')
        await app.state.redis.execute('del', '3')
        yield client


@pytest.mark.asyncio
async def test_post(client):
    s = 'Some important message'
    ttl = 10
    timeout = 1

    res1 = await client.post(
        '/messages/1',
        headers = {
            'Content-Type': 'application/json'
        },
        json={
            'value': s,
            'ttl': ttl,
        }
    )

    assert res1.status_code == 200

    res2 = await client.post(
        '/messages/1',
        headers = {
            'Content-Type': 'application/json'
        },
        json={
            'value': s,
            'ttl': ttl,
        }
    )

    assert res2.status_code == 409


@pytest.mark.asyncio
async def test_get_after_post(client):
    s = 'Some important message'
    ttl = 30
    timeout = 1

    await client.post(
        '/messages/2',
        headers = {
            'Content-Type': 'application/json'
        },
        json={
            'value': s,
            'ttl': ttl,
        }
    )

    for _ in range(10_000):
        res = await client.get('/messages/2', params={'timeout': timeout})
        data = res.json()
        assert res.status_code == 200
        assert data['message'] == s



@pytest.mark.asyncio
async def test_get_before_post(client):
    s = 'Some important message'
    ttl = 30
    timeout = 10
    sleep_time = 5

    async def helper_fn():
        await asyncio.sleep(sleep_time)
        await client.post(
            '/messages/3',
            headers = {
                'Content-Type': 'application/json'
            },
            json={
                'value': s,
                'ttl': ttl,
            }
        )
    
    asyncio.create_task(helper_fn())

    for _ in range(100):
        res = await client.get('/messages/3', params={'timeout': timeout})
        data = res.json()
        assert res.status_code == 200
        assert data['message'] == s


@pytest.mark.asyncio
async def test_get_without_post_timeout(client):
    timeout = 5

    res = await client.get('/messages/4', params={'timeout': timeout})
    data = res.json()
    assert res.status_code == 404
    assert data['detail'] == 'Message with given key not found.'


@pytest.mark.asyncio
async def test_get_without_post_no_timeout(client):
    res = await client.get('/messages/5')
    data = res.json()
    assert res.status_code == 404
    assert data['detail'] == 'Message with given key not found.'
