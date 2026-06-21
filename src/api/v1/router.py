from fastapi import APIRouter

from src.api.v1.booking import router as booking_router
from src.api.v1.schedule import router as schedule_router
from src.api.v1.slot_cron import router as slotcron_router
from src.api.v1.room import router as room_router
from src.api.v1.slot import router as slot_router
from src.auth.router import router as auth_router
from src.api.v1.info import router as info_router

api_router = APIRouter()


api_router.include_router(slot_router, prefix="/slots", tags=["slot"])
api_router.include_router(room_router, prefix="/rooms", tags=["room"])
api_router.include_router(booking_router, prefix="/bookings", tags=["booking"])
api_router.include_router(schedule_router, prefix="/schedules", tags=["schedule"])
api_router.include_router(slotcron_router, prefix="/slotcron", tags=["slotcron"])
api_router.include_router(auth_router, prefix="")
api_router.include_router(info_router, prefix="")