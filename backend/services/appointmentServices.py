from datetime import date, datetime, time
from uuid import UUID

from sqlalchemy.orm import Session

from backend.models.appointment import Appointment, AppointmentStatus
from backend.models.doctor import Doctor
from backend.models.patient import Patient
from backend.models.working_hours import WorkingHours
from backend.schemas.appointment import AppointmentCreate
from backend.utils.slotGenerator import (combine_date_and_time, generate_time_slots, is_past_slot,)


class AppointmentService:
    def __init__(self, db: Session):
        self.db = db

    def get_available_slots(
        self,
        doctor_id: UUID,
        appointment_date: date,
    ):
        """
        Returns all available 30-minute slots for a doctor
        on the requested date.
        """

        doctor = (
            self.db.query(Doctor)
            .filter(Doctor.id == doctor_id)
            .first()
        )

        if doctor is None:
            return None

        weekday = appointment_date.weekday()

        working_hours = (
            self.db.query(WorkingHours)
            .filter(
                WorkingHours.doctor_id == doctor_id,
                WorkingHours.weekday == weekday,
            )
            .first()
        )

        if working_hours is None:
            return []

        slots = generate_time_slots(
            working_hours.start_time,
            working_hours.end_time,
        )

        start_of_day = datetime.combine(
            appointment_date,
            time.min,
        )

        end_of_day = datetime.combine(
            appointment_date,
            time.max,
        )

        booked_appointments = (
            self.db.query(Appointment)
            .filter(
                Appointment.doctor_id == doctor_id,
                Appointment.status == AppointmentStatus.BOOKED,
                Appointment.appointment_time >= start_of_day,
                Appointment.appointment_time <= end_of_day,
            )
            .all()
        )

        booked_slots = {
            appointment.appointment_time
            for appointment in booked_appointments
        }

        available_slots = []

        for slot in slots:
            slot_datetime = combine_date_and_time(
                appointment_date,
                slot,
            )

            if slot_datetime in booked_slots:
                continue

            if is_past_slot(slot_datetime):
                continue

            available_slots.append(slot_datetime)

        return available_slots

# Book appointment
    def book_appointment( self, request: AppointmentCreate ):
        """
        Creates a new appointment after validating:
        - doctor exists
        - patient exists (or creates one)
        - appointment is not in the past
        - slot is available
        """
        try:
            doctor = (
                self.db.query(Doctor)
                .filter(Doctor.id == request.doctor_id)
                .first()
            )

            if doctor is None:
                raise ValueError("Doctor not found.")

            patient = (
                self.db.query(Patient)
                .filter(Patient.email == request.patient_email)
                .first()
            )

            if patient is None:
                patient = Patient(
                name=request.patient_name,
                email=request.patient_email,
                phone=request.patient_phone,
            )

                self.db.add(patient)
                self.db.flush()  # Generates the patient ID without committing
            # validation...

            appointment = Appointment(
                doctor_id=doctor.id,
                patient_id=patient.id,
                appointment_time=request.appointment_time,
                status=AppointmentStatus.BOOKED,
            )

            self.db.add(appointment)
            self.db.commit()
            self.db.refresh(appointment)

            return appointment

        except Exception:
            self.db.rollback()
            raise

        if request.appointment_time < datetime.now():
            raise ValueError("Cannot book an appointment in the past.")

        available_slots = self.get_available_slots(
            request.doctor_id,
            request.appointment_time.date(),
        )

        if available_slots is None:
            raise ValueError("Doctor not found.")

        if request.appointment_time not in available_slots:
            raise ValueError("Selected appointment slot is unavailable.")

        appointment = Appointment(
            doctor_id=doctor.id,
            patient_id=patient.id,
            appointment_time=request.appointment_time,
            status=AppointmentStatus.BOOKED,
        )

        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)

        return appointment
    
# cancel appointment
    def cancel_appointment(
        self,
        appointment_id: UUID,
        reason: str,
    ):
        try:

            appointment = (
                self.db.query(Appointment)
                .filter(Appointment.id == appointment_id)
                .first()
            )

            if appointment is None:
                raise ValueError("Appointment not found.")

            if appointment.status == AppointmentStatus.CANCELLED:
                raise ValueError("Appointment has already been cancelled.")

            appointment.status = AppointmentStatus.CANCELLED
            appointment.cancel_reason = reason

            self.db.commit()
            self.db.refresh(appointment)

            return appointment

        except Exception:
            self.db.rollback()
            raise

# reschedule appointment
    def reschedule_appointment(
        self,
        appointment_id: UUID,
        new_appointment_time: datetime,
    ):
        try:

            appointment = (
                self.db.query(Appointment)
                .filter(Appointment.id == appointment_id)
                .first()
            )

            if appointment is None:
                raise ValueError("Appointment not found.")

            if appointment.status == AppointmentStatus.CANCELLED:
                raise ValueError("Cancelled appointments cannot be rescheduled.")

            if new_appointment_time < datetime.now():
                raise ValueError("Cannot reschedule to a past time.")

            available_slots = self.get_available_slots(
                appointment.doctor_id,
                new_appointment_time.date(),
            )

            if available_slots is None:
                raise ValueError("Doctor not found.")

            if new_appointment_time not in available_slots:
                raise ValueError("Selected slot is unavailable.")

            appointment.appointment_time = new_appointment_time

            self.db.commit()
            self.db.refresh(appointment)

            return appointment

        except Exception:
            self.db.rollback()
            raise