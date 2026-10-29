# Student Name: Ruvi Kathiriya

# Student ID: ET21BTAI031

# Course: Web Programming

# Academic Year: Third Year B.Tech (AI & DS)

# Semester: 6

# Group: 15
from app.pipeline.cleaning import clean


def rec(**kw):
    base = {
        "title": "A Book", "product_url": "http://x/a", "price": "£10.50", "rating": "Three",
        "availability": "In stock (5 available)", "image_url": "http://x/a.jpg",
        "category": "Poetry", "description": "Nice.",
    }
    base.update(kw)
    return base


def test_normalises_price_rating_and_stock():
    df, report = clean([rec(price="Â£51.77", rating="Five", availability="  In   stock (22 available) ")])
    row = df.iloc[0]
    assert row["price"] == 51.77
    assert row["rating"] == 5
    assert bool(row["in_stock"]) is True
    assert row["stock_count"] == 22
    assert report["rows_out"] == 1


def test_drops_duplicates_invalid_price_and_missing_title():
    raw = [
        rec(),
        rec(),                                            # duplicate url
        rec(product_url="http://x/b", price="n/a"),       # invalid price
        rec(product_url="http://x/c", price="£0.00"),     # non-positive price
        rec(product_url="http://x/d", title=""),          # missing title
    ]
    df, report = clean(raw)
    assert len(df) == 1
    assert report["dropped_duplicates"] == 1
    assert report["dropped_invalid_price"] == 2
    assert report["dropped_missing_fields"] == 1
    assert report["rows_dropped"] == 4


def test_incomplete_records_are_kept_with_defaults():
    df, report = clean([rec(category=None, rating="banana", description=None, availability="Out of stock")])
    row = df.iloc[0]
    assert row["category"] == "Uncategorized"
    assert row["rating"] is None or str(row["rating"]) == "<NA>"
    assert bool(row["in_stock"]) is False
    assert row["stock_count"] == 0
    assert report["rating_missing"] == 1
    assert report["category_missing"] == 1


def test_empty_input():
    df, report = clean([])
    assert df.empty
    assert report["rows_in"] == 0
