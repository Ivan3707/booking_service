from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Импортируем ВСЕ наши роутеры
from src.api.v1.booking import router as booking_router
from src.api.v1.schedule import router as schedule_router
from src.api.v1.slot_cron import router as cron_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Booking Service API",
        description="Полный бэкенд для бронирования переговорок (Чистая Архитектура)",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключаем всю нашу артиллерию к API v1
    app.include_router(booking_router, prefix="/api/v1")
    app.include_router(schedule_router, prefix="/api/v1")
    app.include_router(cron_router, prefix="/api/v1")

    @app.get("/healthcheck", tags=["Системные"])
    async def healthcheck():
        return {"status": "ok", "message": "Система работает в штатном режиме"}

    return app

app = create_app()


if __name__ == "__main__":
    # Запускаем uvicorn программно
    uvicorn.run(
        "main:app",  # Пишем строкой, чтобы работал reload!
        host="127.0.0.1",
        port=8000,
        reload=True
    )