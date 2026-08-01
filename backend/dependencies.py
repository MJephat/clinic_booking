# It lets you verify your seeded data.
# The frontend (or Swagger) can easily discover doctor IDs.
from collections.abc import Generator

from sqlalchemy.orm import Session

from backend.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()