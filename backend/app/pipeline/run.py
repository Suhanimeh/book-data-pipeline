#  Student Name: Suhani Mehta
#  Student ID: ET21BTAI042
#  Course: Web Programming
#  Academic Year: Third Year B.Tech (AI & DS)
#  Semester: 6
#  Group: 15

import logging

from ..config import settings
from ..database import SessionLocal, init_db
from ..models import PipelineRun, utcnow
from ..scraper.scraper import scrape_books
from .cleaning import clean
from .store import upsert_books

log = logging.getLogger(__name__)


def create_run() -> int:
    with SessionLocal() as db:
        run = PipelineRun(status="running")
        db.add(run)
        db.commit()
        return run.id


def run_pipeline(run_id: int | None = None) -> None:
    run_id = run_id or create_run()
    db = SessionLocal()
    try:
        raw = scrape_books(settings.scrape_base_url, settings.scrape_max_pages, settings.request_delay)
        df, report = clean(raw)
        log.info("Cleaning report: %s", report)
        stored = upsert_books(db, df)

        run = db.get(PipelineRun, run_id)
        run.status = "success"
        run.rows_scraped = report["rows_in"]
        run.rows_stored = stored
        run.rows_dropped = report["rows_dropped"]
    except Exception as exc:  # noqa: BLE001
        log.exception("Pipeline failed")
        db.rollback()
        run = db.get(PipelineRun, run_id)
        run.status = "failed"
        run.error = str(exc)[:1000]
    finally:
        run.finished_at = utcnow()
        db.commit()
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
    run_pipeline()
