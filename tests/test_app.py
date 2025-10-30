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
async def test_create_and_crud_item_requires_auth_for_rud():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create
        create = await ac.post("/items", json={"name": "widget", "qty": 2})
        assert create.status_code == 200
        item_id = create.json()["id"]

        # Read without auth fails
        noauth = await ac.get(f"/items/{item_id}")
        assert noauth.status_code == 401

        # Read with auth succeeds
        read = await ac.get(f"/items/{item_id}", headers={"Authorization": "Bearer testtoken"})
        assert read.status_code == 200
        assert read.json()["item"]["name"] == "widget"

        # Update
        upd = await ac.put(
            f"/items/{item_id}",
            json={"name": "renamed", "qty": 3},
            headers={"Authorization": "Bearer testtoken"},
        )
        assert upd.status_code == 200
        assert upd.json()["item"]["name"] == "renamed"

        # Delete
        dele = await ac.delete(
            f"/items/{item_id}",
            headers={"Authorization": "Bearer testtoken"},
        )
        assert dele.status_code == 200

        # Verify deleted
        missing = await ac.get(f"/items/{item_id}", headers={"Authorization": "Bearer testtoken"})
        assert missing.status_code == 404
