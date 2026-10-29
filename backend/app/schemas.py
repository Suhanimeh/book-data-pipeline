# Student Name: Ruchita Jain

# Student ID: ET21BTAI022

# Course: Web Programming

# Program: Third Year B.Tech (AI & DS)

# Semester: 6

# Group: 15 


from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category: str
    price: float
    rating: int | None
    in_stock: bool
    stock_count: int
    product_url: str
    image_url: str | None
    description: str | None
    scraped_at: datetime


class BookPage(BaseModel):
    items: list[BookOut]
    total: int
    page: int
    page_size: int
    pages: int


class RunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    started_at: datetime
    finished_at: datetime | None
    rows_scraped: int
    rows_stored: int
    rows_dropped: int
    error: str | None


class CategoryOut(BaseModel):
    name: str
    count: int
