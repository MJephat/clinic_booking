import uuid
from sqlalchemy import Uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from backend.database import Base


class AppointmentStatus(str, Enum):
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    doctor_id: Mapped[int] = mapped_column( ForeignKey("doctors.id", ondelete="CASCADE"))
    patient_id: Mapped[int] = mapped_column( ForeignKey("patients.id", ondelete="CASCADE"))
    appointment_time: Mapped[datetime] = mapped_column(  DateTime,  nullable=False, index=True)

    status: Mapped[AppointmentStatus] = mapped_column( SqlEnum(AppointmentStatus), default=AppointmentStatus.BOOKED, nullable=False)
    cancel_reason: Mapped[str | None] = mapped_column( String(255), nullable=True )

    created_at: Mapped[datetime] = mapped_column( DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column( DateTime, default=datetime.utcnow, onupdate=datetime.utcnow )
# relation
    doctor = relationship( "Doctor", back_populates="appointments" )
    patient = relationship( "Patient", back_populates="appointments")