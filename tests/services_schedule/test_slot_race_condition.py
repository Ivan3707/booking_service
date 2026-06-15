import asyncio
import pytest
from datetime import date, time

from src.repositories.unitofwork import UnitOfWork
from src.services.schedule import ScheduleService
from src.schemas.schedule import ScheduleCreateSchema


@pytest.mark.asyncio
async def test_slot_race_condition():
    service = ScheduleService()

    # ----------------------------
    # 1. SETUP (ОТДЕЛЬНАЯ ТРАНЗАКЦИЯ)
    # ----------------------------
    async with UnitOfWork() as uow:
        room = await uow.rooms.create(
            name="Room",
            description="test",
            capacity=10
        )
        room_id = room.id

    # ----------------------------
    # 2. INPUT SCHEMA ДЛЯ ТЕСТА
    # ----------------------------
    schema = ScheduleCreateSchema(
        room_id=room_id,
        day_of_week=date.today().weekday(),
        start_time=time(9, 0),
        end_time=time(10, 0)
    )

    # ----------------------------
    # 3. CONCURRENT EXECUTION
    # ----------------------------
    async def run():
        async with UnitOfWork() as uow:
            return await service.create_schedule_with_slots(uow, schema)

    await asyncio.gather(run(), run())

    # ----------------------------
    # 4. ASSERT (НОВАЯ СЕССИЯ)
    # ----------------------------
    async with UnitOfWork() as uow:
        slots = await uow.slots.get_by_room(room_id)

    assert len(slots) > 0
    assert len(slots) == len(set(s.start_at for s in slots))