from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# PostgreSQL Connection
# Format: postgresql://<username>:<password>@<host>:<port>/<database_name>
# Example: postgresql://postgres:password@localhost:5432/agriguard
SQLALCHEMY_DATABASE_URL = "postgresql://samarthyajambavalikar:1234@localhost:5432/agriguard"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
