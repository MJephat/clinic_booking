from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.dependencies import get_db
from backend.models.doctor import Doctor
from backend.schemas.doctor import DoctorResponse

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/", response_model=list[DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).order_by(Doctor.name).all()