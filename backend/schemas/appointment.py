from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

# create appointment schema
class AppointmentCreate(BaseModel):
    patient_name: str = Field(..., min_length=2, max_length=100)
    patient_email: EmailStr
    patient_phone: str = Field(..., min_length=10, max_length=20)

    doctor_id: UUID
    appointment_time: datetime

# cancel appointment schema
class AppointmentCancel(BaseModel):
    reason: str = Field(..., min_length=5, max_length=255)

# reschedule appointment schema
class AppointmentReschedule(BaseModel):
    new_appointment_time: datetime

# appointment response schema
class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    doctor_id: UUID
    patient_id: UUID
    appointment_time: datetime
    status: str
    cancel_reason: str | None