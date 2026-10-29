# Book Market Explorer: Data Collection & Analytics Pipeline

An end-to-end data project: **scrape → clean → store → serve → visualise**, containerised with Docker.

| Stage | Technology | Where |
|---|---|---|
| Web scraping | Python, `requests`, **BeautifulSoup** | `backend/app/scraper/scraper.py` |
| Cleaning, transformation, validation | **Pandas** | `backend/app/pipeline/cleaning.py` |
| Storage | **PostgreSQL** (SQLAlchemy, idempotent upserts, indexes) | `backend/app/models.py`, `pipeline/store.py` |
| REST API | **FastAPI** (filtering, sorting, pagination, stats) | `backend/app/routers/` |
| UI | **React** (Vite, Recharts) | `frontend/src/` |
| Deployment | **Docker** + docker-compose (Postgres, API, Nginx) | `docker-compose.yml` |

The data source is [books.toscrape.com](https://books.toscrape.com), a sandbox site made for scraping practice.
For each book the pipeline collects title, price, rating, stock, category and description.

## Quick start (Docker)

```bash
git clone <your-repo-url> && cd book-data-pipeline
cp .env.example .env          # optional
docker compose up --build
```

Then open:

- **UI:** http://localhost:3000
- **API docs (Swagger):** http://localhost:8000/docs

On first start the database is empty, so the API triggers a scrape automatically
(`AUTO_SEED=true`, 5 pages = 100 books, about a minute). You can re-run it any time from the UI
(**Collect data** button) or with `POST /api/pipeline/run`. Set `SCRAPE_MAX_PAGES=50` for the full catalogue.

## How the pipeline works

1. **Scrape.** Walks catalogue pages, then each book's detail page (category, exact stock, description).
   Retries failed requests, waits between requests, and keeps incomplete records rather than crashing.
2. **Clean and validate (Pandas).** Collapses whitespace; strips currency symbols and encoding junk
   (`Â£51.77` → `51.77`); converts rating words (`Three` → `3`); parses `In stock (22 available)` into
   `in_stock` and `stock_count`; fills missing categories with `Uncategorized`; nulls out-of-range ratings;
   drops duplicates, rows without title or URL, and rows with a missing or non-positive price.
   A report of every drop is logged and stored per run.
3. **Store.** Upserts into PostgreSQL keyed on `product_url`, so re-running updates rows instead of duplicating.
   Indexes exist on the columns the API filters and sorts by. Each run is logged in `pipeline_runs`.
4. **Serve.** FastAPI endpoints for the data and for aggregated trends.
5. **Explore.** The React app shows headline numbers, three trend charts, and a filterable, sortable,
   paginated table with expandable descriptions.

## API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/books` | Query params: `search`, `category`, `min_price`, `max_price`, `rating` (minimum), `in_stock`, `sort_by`, `order`, `page`, `page_size` |
| GET | `/api/books/{id}` | Single book |
| GET | `/api/categories` | Categories with counts |
| GET | `/api/stats` | Totals, averages, price histogram, breakdown by category and rating |
| POST | `/api/pipeline/run` | Start a scrape in the background (409 if one is already running) |
| GET | `/api/pipeline/runs` | Recent runs with scraped / stored / dropped counts |
| GET | `/health` | Liveness check |

Example: `curl "http://localhost:8000/api/books?category=Poetry&min_price=10&rating=4&sort_by=price&order=desc"`

## Local development (without Docker)

```bash
# 1. Database
docker run -d --name books-db -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=books postgres:16-alpine

# 2. Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/books
uvicorn app.main:app --reload          # http://localhost:8000/docs
python -m app.pipeline.run             # run the pipeline from the command line

# 3. Frontend (new terminal)
cd frontend
npm install
npm run dev                            # http://localhost:5173 (proxies /api to :8000)
```

## Tests

```bash
cd backend && pytest -q
```

The tests cover the Pandas cleaning rules and the BeautifulSoup parsers (offline, using sample HTML).
GitHub Actions (`.github/workflows/ci.yml`) runs them and builds the frontend on every push.

## Project layout

```
book-data-pipeline/
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py            FastAPI app, CORS, startup seeding
│   │   ├── config.py          Environment-driven settings
│   │   ├── database.py        Engine, session, table creation
│   │   ├── models.py          Book, PipelineRun
│   │   ├── schemas.py         Pydantic response models
│   │   ├── scraper/scraper.py
│   │   ├── pipeline/          cleaning.py, store.py, run.py
│   │   └── routers/           books.py, pipeline.py
│   └── tests/
└── frontend/
    ├── Dockerfile             Build with Node, serve with Nginx
    ├── nginx.conf             Serves the SPA, proxies /api to the backend
    └── src/                   App, api client, components, styles
```

## Notes

- Be polite when scraping: the delay between requests is configurable (`REQUEST_DELAY`). To point the
  scraper at another site, adapt the selectors in `scraper.py` and the rules in `cleaning.py`.
- Tables are created on startup with `create_all`. For production schema changes, add Alembic migrations.
- Change the default database password before deploying anywhere public.

## License

MIT
