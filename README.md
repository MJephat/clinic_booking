# clinic_booking
A RESTful clinic appointment booking system built with FastAPI, PostgreSQL, SQLAlchemy, and Alembic. The API allows patients to book, cancel, and reschedule appointments while ensuring doctors cannot be double-booked and appointments are only made during working hours.

## Live Application
https://clinic-booking-0fv5.onrender.com

## API Documentation
once deployed, the interactive API documentaion is available at:
https://clinic-booking-0fv5.onrender.com/docs

The OpenAPI specification is available at:
https://clinic-booking-0fv5.onrender.com/openapi.json

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
    git clone https://github.com/MJephat/clinic_booking.git
    cd clinic_booking

    python -m venv venv

# Windows
    source venv\Scripts\activate

# Linux
    source venv/bin/activate

    pip install -r requirements.txt
    
    python -m backend.seed.seed_data

    alembic upgrade head

    uvicorn backend.main:app --reload

    The API will be available at:

    http://127.0.0.1:8000

    Swagger documentation:

    http://127.0.0.1:8000/docs

## AI Usage
1. I used AI as a development assistant throughout the project to:
    Brainstorm and document the initial system design,db model,API components and architectural decisions.
    Review and improve the SQLALchemy models, pydantic schemas and routing structure.
    Troubleshoot issues in Alembic migration errors, FastAPI validation errors and PostgreSQL enum conflicts.
    Deployment instructions and GitHub Action CI workflow.

2. One example where an AI suggestion improved your work. What did you prompt it with?
    One useful suggestion was adding validation to prevent double-booking of appointment slots. The Prompt: "We have a problem with booking. We need to validate active appointments to avoid more than one booking for the same doctor and at the same time."

    AI suggested checking for an existing active appointment before creating a new one by querying appointments with the same doctor, appointment time, and BOOKED status. This prevented multiple patients from booking the same slot and aligned the implementation with the business requirements.

3. One example where AI output was wrong or incomplete and how you caught it.
    An example was an Alembic migration that attempted to recreate an existing PostgreSQL enum (AppointmentStatus). Rather than accepting the generated migration as-is, I investigated the migration history, reset the migrations, and regenerated a clean initial migration.

4. Two decisions you made without AI.
    ## Using UUIDS as the primary Key
    I choose UUIDs instead od auto-incrementing integers because it makes identifiers harder to guess, work well across distributed systems and avoids collision if the application is scaled in future.

    ## Separating business logic into a server layer
    I decided to keep appointment booking, cancellation, rescheduling, and availability calculations inside a dedicated service layer instead of placing the logic directly in the FastAPI routes. This keeps the routers focused on handling HTTP requests, improves maintainability, and makes the business logic easier to test independently.