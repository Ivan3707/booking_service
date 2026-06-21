from fastapi import APIRouter, Depends
from uuid import UUID

from src.api.dependencies import get_uow
from src.core.unitofwork import UnitOfWork
from src.services.booking import BookingService
from src.schemas.booking import BookingCreateSchema
from src.auth.dependencies import require_user

router = APIRouter()

booking_service = BookingService()


@router.post("")
async def create_booking(
    schema: BookingCreateSchema,
    uow: UnitOfWork = Depends(get_uow),
    user=Depends(require_user)
):
    user_id = user["user_id"]

    return await booking_service.create_booking(uow, schema, user_id)


@router.get("/me")
async def get_my_bookings(
    uow: UnitOfWork = Depends(get_uow),
    user=Depends(require_user)
):
    async with uow:
        return await uow.bookings.get_by_user(user["user_id"])


@router.post("/{booking_id}/cancel")
async def cancel_booking(
    booking_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    user=Depends(require_user)
):
    result = await booking_service.cancel_booking(uow, booking_id)

    return {
        "status": "success",
        "booking_id": str(result.id),
        "new_status": result.status
    }
