from datetime import time
from sqlalchemy import ForeignKey
from sqlalchemy import Time
from sqlalchemy import Integer
import uuid
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from backend.database import Base


class WorkingHours(Base):
    __tablename__ = "working_hours"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    doctor_id: Mapped[int] = mapped_column( ForeignKey("doctors.id", ondelete="CASCADE"))

    weekday: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    doctor = relationship( "Doctor",back_populates="working_hours")