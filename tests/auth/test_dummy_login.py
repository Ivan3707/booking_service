import pytest


@pytest.mark.asyncio
async def test_dummy_login_user(client):
    response = await client.post("/dummyLogin", params={"role": "user"})

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data


@pytest.mark.asyncio
async def test_dummy_login_admin(client):
    response = await client.post("/dummyLogin", params={"role": "admin"})

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data


@pytest.mark.asyncio
async def test_dummy_login_invalid_role(client):
    response = await client.post("/dummyLogin", params={"role": "hacker"})

    assert response.status_code == 400