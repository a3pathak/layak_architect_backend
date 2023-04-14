from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from typing import Generator
from sqlalchemy.ext.declarative import declarative_base

POSTGRES_USER="postgres"
POSTGRES_PASSWORD=123456
POSTGRES_SERVER="localhost"
POSTGRES_PORT=5432
POSTGRES_DB="ecommerce"

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

SQLALCHEMY_DATABASE_URL = DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

def get_db()-> Generator:
    try: 
        db = SessionLocal()
        yield db
    finally:
        db.close()
