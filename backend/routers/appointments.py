from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from backend.dependencies import get_db
from backend.schemas.appointment import (AppointmentCreate, AppointmentResponse, AppointmentCancel, AppointmentReschedule)
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

@router.patch("/{appointment_id}/cancel", response_model=AppointmentResponse,)
def cancel_appointment( appointment_id: UUID, request: AppointmentCancel, db: Session = Depends(get_db),):
    service = AppointmentService(db)
    try:
        return service.cancel_appointment(
            appointment_id,
            request.reason,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.patch("/{appointment_id}/reschedule", response_model=AppointmentResponse,)
def reschedule_appointment(appointment_id: UUID, request: AppointmentReschedule, db: Session = Depends(get_db),):
    service = AppointmentService(db)
    try:
        return service.reschedule_appointment(
            appointment_id,
            request.new_appointment_time,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )