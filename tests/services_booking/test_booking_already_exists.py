import pytest
from datetime import datetime, timedelta

from src.core.unitofwork import UnitOfWork
from src.schemas.booking import BookingCreateSchema
from src.services.booking import BookingService
from src.core.exceptions import SlotAlreadyBookedException


@pytest.mark.asyncio
async def test_slot_already_booked(sessionmaker):

    service = BookingService()

    async with UnitOfWork(sessionmaker) as uow:
        user1 = await uow.users.create(email="u1@test.com")
        user2 = await uow.users.create(email="u2@test.com")

        room = await uow.rooms.create(
            name="Room",
            description="test",
            capacity=10
        )

        slot = await uow.slots.create(
            room_id=room.id,
            start_at=datetime.utcnow() + timedelta(minutes=10),
            end_at=datetime.utcnow() + timedelta(hours=1)
        )

    # first booking
    async with UnitOfWork(sessionmaker) as uow:
        await service.create_booking(
            uow,
            BookingCreateSchema(slot_id=slot.id),
            user_id=user1.id
        )

    # second must fail
    async with UnitOfWork(sessionmaker) as uow:
        with pytest.raises(SlotAlreadyBookedException):
            await service.create_booking(
                uow,
                BookingCreateSchema(slot_id=slot.id),
                user_id=user2.id
            )