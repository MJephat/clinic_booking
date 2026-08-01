import uuid
from sqlalchemy import Uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialization: Mapped[str] = mapped_column(String(100), nullable=False)
    LicenceNumber: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

# relatioships
    working_hours = relationship("WorkingHours", back_populates="doctor", cascade="all, delete-orphan" )
    appointments = relationship("Appointment",back_populates="doctor",cascade="all, delete-orphan" )