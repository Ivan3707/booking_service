from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.exceptions import (
    BookingAlreadyExistsException,
    ScheduleAlreadyExistsException,
    NotFoundException,
)


async def booking_already_exists_handler(
    request: Request,
    exc: BookingAlreadyExistsException
):
    return JSONResponse(
        status_code=409,
        content={
            "status": "error",
            "message": str(exc) or "Booking already exists"
        }
    )


async def schedule_already_exists_handler(
    request: Request,
    exc: ScheduleAlreadyExistsException
):
    return JSONResponse(
        status_code=409,
        content={
            "status": "error",
            "message": str(exc) or "Schedule already exists"
        }
    )


async def not_found_handler(
    request: Request,
    exc: NotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": str(exc) or "Not found"
        }
    )