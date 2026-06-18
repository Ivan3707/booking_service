from fastapi import FastAPI
import uvicorn

from src.api.v1.router import api_router
from src.api.exceptions import register_exception_handlers

app = FastAPI(
    title="Booking Service",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

register_exception_handlers(app)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )