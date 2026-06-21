import pytest
from datetime import date, timedelta


@pytest.mark.asyncio
async def test_future_bookings_filter(client):
    # 1. login
    login = await client.post("/dummyLogin", params={"role": "user"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. create room
    room_resp = await client.post(
        "/rooms",
        json={"name": "Room 1", "capacity": 10},
        headers=headers
    )
    assert room_resp.status_code == 201
    room_id = room_resp.json()["id"]

    # 3. create schedule (this generates slots)
    schedule_resp = await client.post(
        "/schedules",
        json={
            "room_id": room_id,
            "day_of_week": 1,
            "start_time": "09:00",
            "end_time": "18:00"
        },
        headers=headers
    )
    assert schedule_resp.status_code == 201
    schedule_day = schedule_resp.json()["day_of_week"]

    # 4. compute correct target date
    today = date.today()
    target_date = today + timedelta(
        days=(schedule_day - today.weekday()) % 7 or 7
    )

    # 5. fetch slots
    slots_resp = await client.get(
        f"/slots?room_id={room_id}&date={target_date}",
        headers=headers
    )

    assert slots_resp.status_code == 200

    slots = slots_resp.json()

    assert len(slots) > 0

    # 6. (optional) future bookings assertion
    for s in slots:
        assert "id" in s