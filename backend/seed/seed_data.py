from datetime import time

from backend.database import SessionLocal, init_db
from backend.models.doctor import Doctor
from backend.models.working_hours import WorkingHours

init_db()

db = SessionLocal()

try:
    # Don't seed twice
    if db.query(Doctor).count() > 0:
        print("Doctors already exist.")
        exit()

    doctors = [
        Doctor(name="Dr. John Smith", specialization="General Medicine", LicenceNumber="LIC12345"),
        Doctor(name="Dr. Sarah Johnson", specialization="Pediatrics", LicenceNumber="LIC67890"),
        Doctor(name="Dr. Michael Brown", specialization="Dermatology", LicenceNumber="LIC54321"),
        Doctor(name="Dr. Emily Davis", specialization="Cardiology", LicenceNumber="LIC98765"),
        Doctor(name="Dr. James Wilson", specialization="Orthopedics", LicenceNumber="LIC11111"),
    ]

    db.add_all(doctors)
    db.commit()

    # Refresh so IDs are available
    for doctor in doctors:
        db.refresh(doctor)

    workingHours = []

    for doctor in doctors:
        for weekday in range(5):  # Monday-Friday
            workingHours.append(
                WorkingHours(
                    doctor_id=doctor.id,
                    weekday=weekday,
                    start_time=time(9, 0),
                    end_time=time(17, 0),
                )
            )

    db.add_all(workingHours)
    db.commit()

    print("Doctors and working hours seeded successfully!")

finally:
    db.close()