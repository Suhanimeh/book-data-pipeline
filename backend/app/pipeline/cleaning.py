
#  Student Name: Suhani Mehta
#  Student ID: ET21BTAI042
#  Course: Web Programming
#  Academic Year: Third Year B.Tech (AI & DS)
#  Semester: 6
#  Group: 15

 
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

from datetime import datetime, timezone

import pandas as pd

RAW_COLUMNS = [
    "title", "product_url", "price", "rating", "availability",
    "image_url", "category", "description",
]
FINAL_COLUMNS = [
    "title", "category", "price", "rating", "in_stock", "stock_count",
    "product_url", "image_url", "description", "scraped_at",
]
RATING_MAP = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}


def clean(raw_records: list[dict]) -> tuple[pd.DataFrame, dict]:
    """Return (clean_dataframe, report). Never raises on bad rows; drops and counts them."""
    report = {
        "rows_in": len(raw_records),
        "dropped_missing_fields": 0,
        "dropped_duplicates": 0,
        "dropped_invalid_price": 0,
        "rating_missing": 0,
        "category_missing": 0,
    }
    df = pd.DataFrame(raw_records, columns=RAW_COLUMNS)

    # 1. Normalise text: None -> "", collapse whitespace, strip.
    for col in RAW_COLUMNS:
        df[col] = (
            df[col].fillna("").astype(str)
            .str.replace(r"\s+", " ", regex=True).str.strip()
        )

    # 2. Drop rows missing identity fields.
    n = len(df)
    df = df[(df["title"] != "") & (df["product_url"] != "")].copy()
    report["dropped_missing_fields"] = n - len(df)

    # 3. De-duplicate on the natural key.
    n = len(df)
    df = df.drop_duplicates(subset="product_url", keep="last").copy()
    report["dropped_duplicates"] = n - len(df)

    # 4. Price: "£51.77" / "Â£51.77" / "51,77" -> 51.77, must be a positive number.
    price_text = df["price"].str.replace(",", ".", regex=False).str.replace(r"[^\d.]", "", regex=True)
    df["price"] = pd.to_numeric(price_text, errors="coerce")
    n = len(df)
    df = df[df["price"].notna() & (df["price"] > 0)].copy()
    report["dropped_invalid_price"] = n - len(df)
    df["price"] = df["price"].round(2)

    # 5. Rating: "Three" or "3" -> 3; anything outside 1-5 becomes null (record is kept).
    rating_text = df["rating"].str.lower()
    rating = rating_text.map(RATING_MAP).fillna(pd.to_numeric(rating_text, errors="coerce"))
    rating = rating.where(rating.between(1, 5))
    report["rating_missing"] = int(rating.isna().sum())
    df["rating"] = rating.astype("Int64")

    # 6. Availability -> in_stock flag + stock_count.
    counts = pd.to_numeric(df["availability"].str.extract(r"(\d+)")[0], errors="coerce")
    df["in_stock"] = df["availability"].str.contains("in stock", case=False, regex=False)
    df["stock_count"] = counts.fillna(0).astype(int)
    df.loc[df["in_stock"] & (df["stock_count"] == 0), "stock_count"] = 1  # in stock, count unknown
    df.loc[~df["in_stock"], "stock_count"] = 0

    # 7. Category: fill gaps so every record is filterable.
    missing_cat = df["category"] == ""
    report["category_missing"] = int(missing_cat.sum())
    df.loc[missing_cat, "category"] = "Uncategorized"

    # 8. Empty optional text -> null.
    for col in ("image_url", "description"):
        df[col] = df[col].replace("", None)

    df["scraped_at"] = datetime.now(timezone.utc)
    df = df[FINAL_COLUMNS].reset_index(drop=True)

    report["rows_out"] = len(df)
    report["rows_dropped"] = report["rows_in"] - report["rows_out"]
    return df, report
