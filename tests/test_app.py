import pytest
from httpx import AsyncClient
from app import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/")
        assert resp.status_code == 200
        assert resp.json()["ok"] is True


@pytest.mark.asyncio
async def test_create_item():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/items", json={"name": "widget", "qty": 2})
        assert resp.status_code == 200
        assert resp.json()["item"]["name"] == "widget"
