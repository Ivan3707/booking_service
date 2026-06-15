from fastapi import APIRouter, Depends, HTTPException, status
from src.api.dependencies import get_uow, get_current_admin
from src.repositories.unitofwork import UnitOfWork
from src.services.schedule import ScheduleService
from src.schemas.schedule import ScheduleCreateSchema
from uuid import UUID


router = APIRouter(prefix="/schedules", tags=["Администрирование расписаний"])
schedule_service = ScheduleService()

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schema: ScheduleCreateSchema,
    admin_id: UUID = Depends(get_current_admin),
    uow: UnitOfWork = Depends(get_uow)
):
    """
    Эндпоинт для админов: создает новое еженедельное расписание для комнаты
    и автоматически нарезает сетку слотов на 30 дней вперед.
    """
    try:
        schedule = await schedule_service.admin_create_schedule_with_slots(uow=uow, schema=schema)
        return {
            "status": "success",
            "data": {
                "schedule_id": schedule.id,
                "room_id": schedule.room_id,
                "day_of_week": schedule.day_of_week
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании расписания: {str(e)}"
        )