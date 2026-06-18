from fastapi import FastAPI

from .handlers import (
    booking_already_exists_handler,
    schedule_already_exists_handler,
    not_found_handler,
)

from src.core.exceptions import (
    BookingAlreadyExistsException,
    ScheduleAlreadyExistsException,
    NotFoundException,
)


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        BookingAlreadyExistsException,
        booking_already_exists_handler
    )

    app.add_exception_handler(
        ScheduleAlreadyExistsException,
        schedule_already_exists_handler
    )

    app.add_exception_handler(
        NotFoundException,
        not_found_handler
    )