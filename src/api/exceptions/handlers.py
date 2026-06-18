from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.exceptions import (
    BookingAlreadyExistsException,
    ScheduleAlreadyExistsException,
    NotFoundException,
    SlotAlreadyBookedException,
    SlotNotFoundException,
    BadRequestException,
)



async def booking_already_exists_handler(
    request: Request,
    exc: BookingAlreadyExistsException
):
    return JSONResponse(
        status_code=409,
        content={
            "status": "error",
            "message": str(exc)
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
            "message": str(exc)
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
            "message": str(exc) 
        }
    )

async def slot_already_booked_handler(
    request: Request,
    exc: SlotAlreadyBookedException
):
    return JSONResponse(
        status_code=409,
        content={
            "status": "error",
            "message": str(exc)
        }
    )


async def slot_not_found_handler(
    request: Request,
    exc: SlotNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": str(exc)
        }
    )


async def bad_request_handler(
    request: Request,
    exc: BadRequestException
):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": str(exc)
        }
    )