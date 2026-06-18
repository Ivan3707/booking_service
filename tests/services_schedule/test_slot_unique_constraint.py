import pytest
from datetime import datetime, timedelta

from src.core.unitofwork import UnitOfWork
from src.models.models import Slot


@pytest.mark.asyncio
async def test_slot_unique_constraint(sessionmaker):

    async with UnitOfWork(sessionmaker) as uow:
        room = await uow.rooms.create(
            name="Room",
            description="test",
            capacity=10
        )

        slot_time = datetime.utcnow() + timedelta(days=1)

        slot = Slot(
            room_id=room.id,
            start_at=slot_time,
            end_at=slot_time + timedelta(minutes=30)
        )

        await uow.slots.add_bulk_safe([slot])

        await uow.slots.add_bulk_safe([slot])

        slots = await uow.slots.get_by_room(room.id)

        assert len(slots) == 1