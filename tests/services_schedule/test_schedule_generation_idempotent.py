import pytest
from datetime import date, time

from src.repositories.unitofwork import UnitOfWork
from src.services.schedule import ScheduleService
from src.schemas.schedule import ScheduleCreateSchema

@pytest.mark.asyncio
async def test_schedule_generation_idempotent():
    service = ScheduleService()

    async with UnitOfWork() as uow:
        room = await uow.rooms.create(
            name="Room",
            description="test",
            capacity=10
        )

        schema = ScheduleCreateSchema(
            room_id=room.id,
            day_of_week=date.today().weekday(),
            start_time=time(9, 0),
            end_time=time(10, 0)
        )

        await service.create_schedule_with_slots(uow, schema)
        await service.create_schedule_with_slots(uow, schema)

        slots = await uow.slots.get_by_room(room.id)

        assert len(slots) == len(set(s.start_at for s in slots))