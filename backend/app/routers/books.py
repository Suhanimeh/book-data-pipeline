
#  Student Name: Suhani Mehta
#  Student ID: ET21BTAI042
#  Course: Web Programming
#  Academic Year: Third Year B.Tech (AI & DS)
#  Semester: 6
#  Group: 15

import math
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Book
from ..schemas import BookOut, BookPage, CategoryOut

router = APIRouter(prefix="/api", tags=["books"])

SORTABLE = {
    "title": Book.title,
    "price": Book.price,
    "rating": Book.rating,
    "category": Book.category,
    "stock_count": Book.stock_count,
    "scraped_at": Book.scraped_at,
}


@router.get("/books", response_model=BookPage)
def list_books(
    search: str | None = Query(None, description="Case-insensitive match on title"),
    category: str | None = None,
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    rating: int | None = Query(None, ge=1, le=5, description="Minimum rating"),
    in_stock: bool | None = None,
    sort_by: Literal["title", "price", "rating", "category", "stock_count", "scraped_at"] = "title",
    order: Literal["asc", "desc"] = "asc",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    filters = []
    if search:
        filters.append(Book.title.ilike(f"%{search}%"))
    if category:
        filters.append(Book.category == category)
    if min_price is not None:
        filters.append(Book.price >= min_price)
    if max_price is not None:
        filters.append(Book.price <= max_price)
    if rating is not None:
        filters.append(Book.rating >= rating)
    if in_stock is not None:
        filters.append(Book.in_stock == in_stock)

    total = db.scalar(select(func.count(Book.id)).where(*filters)) or 0
    col = SORTABLE[sort_by]
    ordering = col.desc().nulls_last() if order == "desc" else col.asc().nulls_last()
    items = db.scalars(
        select(Book).where(*filters).order_by(ordering, Book.id)
        .offset((page - 1) * page_size).limit(page_size)
    ).all()

    return BookPage(
        items=items, total=total, page=page, page_size=page_size,
        pages=max(1, math.ceil(total / page_size)),
    )


@router.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    rows = db.execute(
        select(Book.category, func.count(Book.id)).group_by(Book.category).order_by(Book.category)
    ).all()
    return [CategoryOut(name=n, count=c) for n, c in rows]


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    total, avg_price, min_price, max_price, in_stock, last_updated = db.execute(
        select(
            func.count(Book.id),
            func.avg(Book.price),
            func.min(Book.price),
            func.max(Book.price),
            func.sum(case((Book.in_stock, 1), else_=0)),
            func.max(Book.scraped_at),
        )
    ).one()

    by_category = db.execute(
        select(Book.category, func.count(Book.id), func.avg(Book.price))
        .group_by(Book.category).order_by(func.count(Book.id).desc(), Book.category)
    ).all()

    by_rating = db.execute(
        select(Book.rating, func.count(Book.id), func.avg(Book.price))
        .where(Book.rating.is_not(None)).group_by(Book.rating).order_by(Book.rating)
    ).all()

    bucket = func.floor(Book.price / 10)
    histogram = db.execute(
        select(bucket, func.count(Book.id)).group_by(bucket).order_by(bucket)
    ).all()

    return {
        "total_books": total,
        "avg_price": round(float(avg_price or 0), 2),
        "min_price": float(min_price or 0),
        "max_price": float(max_price or 0),
        "in_stock": int(in_stock or 0),
        "last_updated": last_updated,
        "by_category": [
            {"category": c, "count": n, "avg_price": round(float(a), 2)} for c, n, a in by_category
        ],
        "by_rating": [
            {"rating": r, "count": n, "avg_price": round(float(a), 2)} for r, n, a in by_rating
        ],
        "price_histogram": [
            {"range": f"£{int(b) * 10}-{int(b) * 10 + 10}", "count": n} for b, n in histogram
        ],
    }
