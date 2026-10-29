
#  Student Name: Suhani Mehta
#  Student ID: ET21BTAI042
#  Course: Web Programming
#  Academic Year: Third Year B.Tech (AI & DS)
#  Semester: 6
#  Group: 15

import logging
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select

from .config import settings
from .database import SessionLocal, init_db
from .models import Book
from .pipeline.run import create_run, run_pipeline
from .routers import books, pipeline

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    if settings.auto_seed:
        with SessionLocal() as db:
            empty = (db.scalar(select(func.count(Book.id))) or 0) == 0
        if empty:
            run_id = create_run()
            threading.Thread(target=run_pipeline, args=(run_id,), daemon=True).start()
    yield


app = FastAPI(
    title="Book Data Pipeline API",
    description="Serves books scraped, cleaned and stored by the pipeline.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(pipeline.router)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}
