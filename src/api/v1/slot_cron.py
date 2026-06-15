from fastapi import APIRouter, Depends, status
from src.api.dependencies import get_uow
from src.repositories.unitofwork import UnitOfWork
from src.services.slot_cron import SlotCronService

router = APIRouter(prefix="/cron", tags=["Системные задачи (Cron)"])
cron_service = SlotCronService()

@router.post("/pregenerate-slots", status_code=status.HTTP_200_OK)
async def trigger_daily_slots_generation(uow: UnitOfWork = Depends(get_uow)):
    """
    Ручной триггер ночного робота. 
    Заглядывает на 30 дней вперед и генерирует недостающие слоты.
    """
    await cron_service.cron_daily_pregenerate_slots(uow=uow)
    return {
        "status": "success",
        "message": "Фоновая генерация слотов на 30-й день успешно запущена и завершена"
    }