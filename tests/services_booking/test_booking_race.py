from uuid import uuid4

import pytest
import asyncio
from datetime import datetime, timedelta

from src.core.exceptions import SlotAlreadyBookedException
from src.schemas.booking import BookingCreateSchema
from src.core.unitofwork import UnitOfWork
from src.services.booking import BookingService



@pytest.mark.asyncio
async def test_booking_race_condition(sessionmaker):

    service = BookingService()

    async with UnitOfWork(sessionmaker()) as uow:

        room = await uow.rooms.create(
            name="Test Room",
            description="test",
            capacity=10
        )

        slot = await uow.slots.create(
            room_id=room.id,
            start_at=datetime.utcnow() + timedelta(minutes=10),
            end_at=datetime.utcnow() + timedelta(hours=1)
        )

        user1 = await uow.users.create(
            email="user1@test.com"
        )

        user2 = await uow.users.create(
            email="user2@test.com"
        )

    async def make_booking(user_id):

        async with UnitOfWork(sessionmaker()) as uow:

            return await service.create_booking(
                uow,
                BookingCreateSchema(slot_id=slot.id),
                user_id=user_id
            )

    results = await asyncio.gather(
        make_booking(user1.id),
        make_booking(user2.id),
        return_exceptions=True
    )

    successes = [
        r for r in results
        if not isinstance(r, Exception)
    ]

    errors = [
        r for r in results
        if isinstance(r, Exception)
    ]

    assert len(successes) == 1
    assert len(errors) == 1

    assert isinstance(
        errors[0],
        SlotAlreadyBookedException
    )