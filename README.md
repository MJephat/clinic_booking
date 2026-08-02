# clinic_booking
A RESTful clinic appointment booking system built with FastAPI, PostgreSQL, SQLAlchemy, and Alembic. The API allows patients to book, cancel, and reschedule appointments while ensuring doctors cannot be double-booked and appointments are only made during working hours.

## Live Application
https://clinic-booking-api.example.com

## API Documentation
once deployed, the interactive API documentaion is available at:
https://<your-domain>/docs

The OpenAPI specification is available at:
https://<your-domain>/openapi.json

## Deployment
The application is automatically deployed whenever changes are merged into the:

main branch.

### Deployment Process
The deployment pipeline performs the following steps:

1. Checks out the latest code from the main branch.
2. Installs all Python dependencies.
3. Runs database migrations using Alembic.
4. Executes automated tests (if configured).
5. Builds the application.
6. Deploys the latest version to the hosting platform.
7. Starts the FastAPI application and makes it available through the    public URL.

This ensures every deployment uses the latest database schema and application code.

## CI/CD Pipeline

The project uses a Continuous Integration and Continuous Deployment (CI/CD) pipeline to automate deployments.

The pipeline:

Validates the source code.
Installs project dependencies.
Applies Alembic database migrations.
Runs automated tests (when available).
Deploys the application automatically after a successful build.
Ensures the production environment stays synchronized with the latest stable code.

This approach minimizes manual deployment steps and provides consistent, repeatable releases.

## Technology Stack
  python 3.13
  FastAPI
  PostgreSQL
  SQLAlchemy ORM
  Alembic
  Pydantic
  Uvicorn

## Features
### Required Feature
     Booking appointments
     View doctor avaikability
     Cancel appointments
     Reschedule appointments
     Automatic slot availability update
     Prevent double booking
     validate doctor working hours
     prevent booking appointment in the past

### Bonus Feature
    View upcoming appointment for a patient
    Prevent booking within one hour of the appointment time

## Running the project Locally
    git clone <repository-url>
    cd clinic_booking

    python -m venv venv

    # Windows
    source venv\Scripts\activate

    # Linux
    source venv/bin/activate

    pip install -r requirements.txt

    alembic upgrade head

    uvicorn backend.main:app --reload

    The API will be available at:

    http://127.0.0.1:8000

    Swagger documentation:

    http://127.0.0.1:8000/docs