from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.api.dependencies import get_uow
from src.core.unitofwork import UnitOfWork
from src.services.schedule import ScheduleService
from src.schemas.schedule import ScheduleCreateSchema


router = APIRouter(prefix="/schedules",tags=["schedule"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schema: ScheduleCreateSchema,
    uow: UnitOfWork = Depends(get_uow)
):
    service = ScheduleService()

    schedule = await service.create_schedule_with_slots(
        uow=uow,
        schema=schema
    )

    return {
        "schedule_id": schedule.id,
        "room_id": schedule.room_id,
        "day_of_week": schedule.day_of_week
    }

@router.get("/schedules")
async def get_schedules(
    room_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    async with uow:
        return await uow.schedules.get_by_room(room_id)