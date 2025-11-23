from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# PostgreSQL Connection
# Format: postgresql://<username>:<password>@<host>:<port>/<database_name>
# Example: postgresql://postgres:password@localhost:5432/agriguard
# Default to local Postgres, but allow env var override for Render
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://samarthyajambavalikar:1234@localhost:5432/agriguard")

# Fix for Render's "postgres://" which SQLAlchemy removed support for
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
