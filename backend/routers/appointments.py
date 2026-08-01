from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.dependencies import get_db
from backend.schemas.appointment import (AppointmentCreate, AppointmentResponse)
from backend.services.appointmentServices import AppointmentService


router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentResponse)
def book_appointment( request: AppointmentCreate, db: Session = Depends(get_db),):
    service = AppointmentService(db)
    try:
        return service.book_appointment(request)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )