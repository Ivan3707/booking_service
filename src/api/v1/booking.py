from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from src.api.dependencies import get_uow, get_current_user
from src.repositories.unitofwork import UnitOfWork
from src.services.booking import BookingService
from src.schemas.booking import BookingCreateSchema
from src.core.exceptions import SlotAlreadyBookedException

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

# Создаем экземпляр сервиса (он не хранит состояние, можно один на все запросы)
booking_service = BookingService()

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_booking(
    schema: BookingCreateSchema, 
    user_id: UUID = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    """Эндпоинт для создания бронирования пользователем."""
    try:
        booking = await booking_service.create_booking(uow=uow, schema=schema, user_id=user_id)
        return {
            "status": "success",
            "data": {
                "booking_id": booking.id,
                "user_id": booking.user_id,
                "slot_id": booking.slot_id
            }
        }
    except SlotAlreadyBookedException as e:
        # Перехватываем нашу красивую бизнес-ошибку из сервиса
        # и превращаем её в понятный для фронтенда HTTP-статус 400
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Этот слот уже занят кем-то другим."
        )