import pytest
from datetime import datetime,  timedelta

from src.repositories.unitofwork import UnitOfWork


@pytest.mark.asyncio
async def test_slot_unique_constraint():
    async with UnitOfWork() as uow:
        room = await uow.rooms.create(
            name="Room",
            description="test",
            capacity=10
        )

        slot_time = datetime.utcnow() + timedelta(days=1)

        await uow.slots.add_bulk_safe([
            {
                "room_id": room.id,
                "start_at": slot_time,
                "end_at": slot_time + timedelta(minutes=30)
            }
        ])

        await uow.slots.add_bulk_safe([
            {
                "room_id": room.id,
                "start_at": slot_time,
                "end_at": slot_time + timedelta(minutes=30)
            }
        ])

        slots = await uow.slots.get_by_room(room.id)

        assert len(slots) == 1