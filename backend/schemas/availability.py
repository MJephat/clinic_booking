from datetime import date, datetime
from uuid import UUID


from pydantic import BaseModel


class AvailabilityResponse(BaseModel):
    doctor_id: UUID
    date: date
    available_slots: list[datetime]