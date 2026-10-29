#  Student Name: Ruchita Jain

# Student ID: ET21BTAI022

# Course: Web Programming

# Program: Third Year B.Tech (AI & DS)

# Semester: 6

# Group: 15 

import logging
import time

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings

log = logging.getLogger(__name__)

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(retries: int = 15, delay: float = 2.0) -> None:
    """Create tables, waiting for PostgreSQL to accept connections."""
    from . import models  # noqa: F401  (register models)

    for attempt in range(1, retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError:
            log.warning("Database not ready (attempt %s/%s)", attempt, retries)
            time.sleep(delay)
    raise RuntimeError("Could not connect to the database")
