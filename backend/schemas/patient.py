from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID

class PatientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr