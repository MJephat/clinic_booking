from fastapi import FastAPI

# Import models so SQLAlchemy registers them
from backend import models
from backend.database import Base, engine, init_db
from backend.routers import doctors, appointments

init_db()

app = FastAPI(title="Clinic Booking API")

app.include_router(doctors.router)
app.include_router(appointments.router)