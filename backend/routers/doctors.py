from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from datetime import date
from uuid import UUID

from backend.dependencies import get_db
from backend.models.doctor import Doctor
from backend.schemas.doctor import DoctorResponse
from backend.schemas.availability import AvailabilityResponse
from backend.services.appointmentServices import AppointmentService

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/", response_model=list[DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).order_by(Doctor.name).all()

@router.get( "/{doctor_id}/availability", response_model=AvailabilityResponse,)
def get_availability(doctor_id: UUID, date: date, db: Session = Depends(get_db),
):
    service = AppointmentService(db)
    slots = service.get_available_slots(
        doctor_id,
        date,
    )

    if slots is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    return AvailabilityResponse(
        doctor_id=doctor_id,
        date=date,
        available_slots=slots,
    )