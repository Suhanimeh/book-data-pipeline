# //
#  Student Name: Suhani Mehta and ruchita jain
#  Student ID: ET21BTAI042 and ET21BTAI022
#  Course: Web Programming
#  Academic Year: Third Year B.Tech (AI & DS)
#  Semester: 6
#  Group: 15
# //
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), index=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(8, 2), index=True)
    rating: Mapped[int | None] = mapped_column(Integer, index=True, nullable=True)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    stock_count: Mapped[int] = mapped_column(Integer, default=0)
    product_url: Mapped[str] = mapped_column(String(500), unique=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(20), default="running")  # running|success|failed
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rows_scraped: Mapped[int] = mapped_column(Integer, default=0)
    rows_stored: Mapped[int] = mapped_column(Integer, default=0)
    rows_dropped: Mapped[int] = mapped_column(Integer, default=0)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
