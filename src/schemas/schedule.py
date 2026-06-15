from datetime import time
from pydantic import BaseModel, Field, model_validator
from uuid import UUID

class ScheduleCreateSchema(BaseModel):
    room_id: UUID
    day_of_week: int = Field(..., ge=0, le=6, description="День недели от 0 (Понедельник) до 6 (Воскресенье)")
    start_time: time
    end_time: time

    # Вот она — выделенная, автоматическая валидация данных!
    @model_validator(mode="after")
    def validate_time_range(self) -> "ScheduleCreateSchema":
        if self.start_time >= self.end_time:
            raise ValueError("Время начала расписания не может быть позже или равно времени окончания")
        return self