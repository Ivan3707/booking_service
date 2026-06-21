from fastapi import APIRouter, Depends
from datetime import date
from uuid import UUID

from src.api.dependencies import get_uow
from src.core.unitofwork import UnitOfWork

router = APIRouter()

@router.get("")
async def get_slots(
    room_id: UUID,
    date: date,
    uow: UnitOfWork = Depends(get_uow)
):
    async with uow:
        return await uow.slots.get_by_room_and_date(room_id, date)


@router.get("/available")
async def get_available_slots(
    room_id: UUID,
    date: date,
    uow: UnitOfWork = Depends(get_uow)
):
    async with uow:
        return await uow.slots.get_available_slots(room_id, date)