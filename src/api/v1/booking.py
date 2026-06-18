from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.api.dependencies import get_uow
from src.core.unitofwork import UnitOfWork

from src.services.booking import BookingService
from src.schemas.booking import BookingCreateSchema

TEST_USER_ID = UUID("11111111-1111-1111-1111-111111111111")
router = APIRouter(prefix="/bookings", tags=["booking"])

booking_service = BookingService()


@router.post("/bookings")
async def create_booking(
    schema: BookingCreateSchema,
    uow: UnitOfWork = Depends(get_uow)
):
    user_id = TEST_USER_ID

    return await booking_service.create_booking(uow, schema, user_id)

@router.get("/me")
async def get_my_bookings(
    user_id: UUID,  # пока без JWT
    uow: UnitOfWork = Depends(get_uow)
):
    async with uow:
        return await uow.bookings.get_by_user(user_id)
    
@router.post("/bookings/{booking_id}/cancel")
async def cancel_booking(
    booking_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    result = await booking_service.cancel_booking(uow, booking_id)

    return {
        "status": "success",
        "booking_id": str(result.id),
        "new_status": result.status
    }