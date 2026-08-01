from fastapi import APIRouter

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.get("/")
def get_appointments():
    return {"message": "Appointments endpoint working!"}