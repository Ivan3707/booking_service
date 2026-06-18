from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from src.models.models import BookingStatusEnum
from src.core.unitofwork import UnitOfWork
from sqlalchemy.exc import IntegrityError
from src.core.exceptions import (
    SlotAlreadyBookedException,
    BookingNotFoundException,
    BadRequestException,
    SlotNotFoundException # Нужно добавить для ошибок времени
)

class BookingService:
    async def create_booking(self, uow, schema, user_id):
        slot = await uow.slots.get_by_id(schema.slot_id)
        if not slot:
            raise SlotNotFoundException("Слот не найден")

        # 2. проверка времени
        now = datetime.utcnow()
        if slot.start_at <= now:
            raise BadRequestException("Нельзя бронировать прошедшие слоты")

        # 3. создаём бронь (конкуренция решается БД)
        try:
            return await uow.bookings.create(
                user_id=user_id,
                slot_id=schema.slot_id,
                status=BookingStatusEnum.ACTIVE
            )

        except IntegrityError as e:
            await uow.session.rollback()
            if "uq_booking_active_slot" in str(e.orig):
                raise SlotAlreadyBookedException("Слот уже занят") from e
            raise

    async def cancel_booking(self, uow, booking_id):
        booking = await uow.bookings.get_by_id(booking_id)

        if not booking:
            raise HTTPException(status_code=404, detail="Бронирование не найдено")

        if booking.status == BookingStatusEnum.CANCELLED:
            raise HTTPException(status_code=400, detail="Уже отменено")

        updated = await uow.bookings.cancel(booking_id)

        return updated