from datetime import datetime, timezone
from uuid import UUID
from src.repositories.unitofwork import UnitOfWork
from src.schemas.booking import BookingCreateSchema
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
        if slot.start_at < now:
            raise BadRequestException("Нельзя бронировать прошедшие слоты")

        # 3. создаём бронь (конкуренция решается БД)
        try:
            return await uow.bookings.create(
                user_id=user_id,
                slot_id=schema.slot_id
            )

        except IntegrityError as e:
            raise SlotAlreadyBookedException("Слот уже занят") from e

    async def cancel_booking(self, uow: UnitOfWork, booking_id: UUID, user_id: UUID):
        async with uow:
            result = await uow.bookings.cancel_booking(booking_id, user_id)

            if not result:
                raise BookingNotFoundException()

            return {"status": "success", "message": "Бронирование успешно отменено"}