from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.appointment import AppointmentResponse
from backend.services.appointmentServices import AppointmentService

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("/{patient_id}/appointments", response_model=list[AppointmentResponse],)
def get_patient_appointments(patient_id: UUID, db: Session = Depends(get_db),):
    service = AppointmentService(db)
    return service.get_patient_appointments(patient_id)