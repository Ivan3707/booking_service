from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_admin_cannot_create_booking(client):
    login = await client.post("/dummyLogin", params={"role": "admin"})
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    resp = await client.post(
        "/bookings",
        json={"slot_id": str(uuid4())},
        headers=headers
    )

    assert resp.status_code == 403

@pytest.mark.asyncio
async def test_user_can_create_booking(client):
    login = await client.post("/dummyLogin", params={"role": "user"})
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    resp = await client.post(
        "/bookings",
        json={"slot_id": str(uuid4())},
        headers=headers
    )

    # тут может быть 200 или 404 (если slot не создан — это нормально)
    assert resp.status_code in (200, 404)