import pytest


@pytest.mark.asyncio
async def test_info_endpoint(client):
    response = await client.get("/_info")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}