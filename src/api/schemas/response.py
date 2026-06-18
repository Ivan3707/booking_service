from typing import Any

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    status: str = "success"
    data: Any