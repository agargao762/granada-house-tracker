from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_PATH
from models.house import Base

engine = create_engine(f"sqlite:///{DATABASE_PATH}")

SessionLocal = sessionmaker(bind=engine)


def create_database():
    Base.metadata.create_all(engine)


def get_session():
    return SessionLocal()