# Student Name: Ruvi Kathiriya and ruchita jain

# Student ID: ET21BTAI021 and ET21BTAI022

# Course: Web Programming

# Academic Year: Third Year B.Tech (AI & DS)

# Semester: 6

# Group: 15
import logging
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

HEADERS = {"User-Agent": "book-data-pipeline/1.0 (educational project)"}


def parse_listing(html: str, page_url: str) -> list[dict]:
    """Extract one raw record per book card on a catalogue page."""
    soup = BeautifulSoup(html, "lxml")
    records = []
    for card in soup.select("article.product_pod"):
        link = card.select_one("h3 a")
        if link is None:
            continue
        rating_tag = card.select_one("p.star-rating")
        rating_classes = rating_tag.get("class", []) if rating_tag else []
        price_tag = card.select_one("p.price_color")
        avail_tag = card.select_one("p.availability")
        img_tag = card.select_one("img")
        records.append(
            {
                "title": link.get("title") or link.get_text(strip=True),
                "product_url": urljoin(page_url, link.get("href", "")),
                "price": price_tag.get_text(strip=True) if price_tag else None,
                "rating": next((c for c in rating_classes if c != "star-rating"), None),
                "availability": avail_tag.get_text(" ", strip=True) if avail_tag else None,
                "image_url": urljoin(page_url, img_tag["src"]) if img_tag and img_tag.get("src") else None,
            }
        )
    return records


def parse_detail(html: str) -> dict:
    """Extract category, stock text and description from a book detail page."""
    soup = BeautifulSoup(html, "lxml")
    crumbs = soup.select("ul.breadcrumb li a")
    category = crumbs[-1].get_text(strip=True) if len(crumbs) >= 3 else None

    description = None
    desc_header = soup.select_one("#product_description")
    if desc_header is not None:
        para = desc_header.find_next_sibling("p")
        description = para.get_text(" ", strip=True) if para else None

    avail_tag = soup.select_one("p.availability")
    detail = {"category": category, "description": description}
    if avail_tag is not None:
        # The detail page shows the exact count, e.g. "In stock (22 available)".
        detail["availability"] = avail_tag.get_text(" ", strip=True)
    return detail


def fetch(session: requests.Session, url: str, retries: int = 3) -> str | None:
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(url, timeout=15)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            resp.encoding = "utf-8"
            return resp.text
        except requests.RequestException as exc:
            log.warning("GET %s failed (%s/%s): %s", url, attempt, retries, exc)
            time.sleep(1.5 * attempt)
    return None


def scrape_books(base_url: str, max_pages: int = 5, delay: float = 0.3) -> list[dict]:
    session = requests.Session()
    session.headers.update(HEADERS)
    records: list[dict] = []

    for page in range(1, max_pages + 1):
        page_url = urljoin(base_url, f"catalogue/page-{page}.html")
        html = fetch(session, page_url)
        if html is None:
            log.info("No page at %s, stopping.", page_url)
            break
        items = parse_listing(html, page_url)
        if not items:
            break
        log.info("Page %s: %s books", page, len(items))

        for item in items:
            time.sleep(delay)
            detail_html = fetch(session, item["product_url"])
            if detail_html:
                item.update({k: v for k, v in parse_detail(detail_html).items() if v is not None})
            records.append(item)  # incomplete records are kept; cleaning decides their fate

    log.info("Scraped %s raw records", len(records))
    return records
