# Student Name: Ruvi Kathiriya

# Student ID: ET21BTAI031

# Course: Web Programming

# Academic Year: Third Year B.Tech (AI & DS)

# Semester: 6

# Group: 15
#  Academic Declaration:
#  I declare that this assignment is my own work and has been completed
#  in accordance with Sarvajanik University's Academic Policy. No part
#  of this assignment has been copied manually or electronically from
#  any other source, including websites, or distributed to other students
#  without authorization.
 
#  Acknowledgement:
#  I sincerely thank my professor for providing guidance, support, and
#  valuable feedback throughout this project. Their encouragement and
#  assistance helped us understand the concepts and complete this project
#  successfully.
import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from ..models import Book

UPDATE_COLUMNS = [
    "title", "category", "price", "rating", "in_stock", "stock_count",
    "image_url", "description", "scraped_at",
]


def to_records(df: pd.DataFrame) -> list[dict]:
    """DataFrame -> list of dicts with NaN / <NA> converted to None."""
    return df.astype(object).where(df.notna(), None).to_dict("records")


def upsert_books(db: Session, df: pd.DataFrame, chunk_size: int = 500) -> int:
    """Insert new books and update existing ones (keyed on product_url)."""
    records = to_records(df)
    for i in range(0, len(records), chunk_size):
        stmt = insert(Book).values(records[i : i + chunk_size])
        stmt = stmt.on_conflict_do_update(
            index_elements=["product_url"],
            set_={col: stmt.excluded[col] for col in UPDATE_COLUMNS},
        )
        db.execute(stmt)
    db.commit()
    return len(records)
