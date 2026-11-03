# INDUSTRIAL INTELLIGENCE

A persistent web-based platform to discover Organized Industrial Zones (OSBs) in Türkiye (starting with Bursa), discover manufacturing companies, collect publicly disclosed professional business contacts, save everything to PostgreSQL, remember processed websites and pages, track scraping jobs, and export Excel workbooks.

---

## Architecture Overview

```
                      +-----------------------------------+
                      |   React + TypeScript + Vite UI    |
                      | (Tailwind CSS, Lucide, Dark Mode) |
                      +-----------------+-----------------+
                                        | HTTP / JSON
                                        v
                      +-----------------+-----------------+
                      |     FastAPI Backend (REST API)    |
                      |     SQLAlchemy 2.0 + Pydantic v2  |
                      +-------+-------------------+-------+
                              |                   |
            Async Tasks / Job |                   | Relational Persistence
            Queue             |                   |
                              v                   v
                     +--------+------+    +-------+--------+
                     | Redis 7 + RQ  |    | PostgreSQL 16  |
                     +--------+------+    |  (8 Tables)    |
                              |           +----------------+
                              v
                     +--------+------+
                     | Scraping      |
                     | Worker        |
                     | (HTTPX, BS4,  |
                     |  Playwright)  |
                     +---------------+
```

---

## Normalized Database Schema (PostgreSQL)

The platform implements 8 relational tables with strict foreign keys, composite uniqueness constraints, and B-tree indexes:

| Table | Purpose | Key Constraints & Indexes |
|---|---|---|
| `industrial_zones` | Catalog of Organized Industrial Zones (OSBs) | Unique `name`, Unique `slug`, Index on `province`, `district` |
| `companies` | Discovered industrial manufacturers | Composite Unique (`zone_id`, `normalized_name`), Unique `slug`, FK to `industrial_zones` |
| `contacts` | Public business emails, phones, executive roles | Composite Unique (`company_id`, `contact_type`, `value`), Confidence score, FK to `companies` |
| `websites` | Monitored domains, crawl status, policies | Unique `domain`, Index on `status`, FKs to `industrial_zones` & `companies` |
| `scraped_pages` | Visited pages, normalized URLs, content hash | Composite Unique (`website_id`, `normalized_url`), Index on `content_hash` |
| `scraping_jobs` | Background crawl pipelines & execution status | Index on `status`, Tracks mode (`new_only`, `retry_failed`, `refresh_all`), targets, success/error counts |
| `sources` | Provenance audit trail of extracted facts | Index on (`entity_type`, `entity_id`), raw snippet, HTTP status, retrieval timestamp |
| `data_changes` | Field-level change log for continuous tracking | Index on (`entity_type`, `entity_id`), records `old_value`, `new_value`, reason, timestamp |

---

## Multi-Mode Scraping Support

The platform supports 3 distinct crawl operational modes:
1. **New Websites Only (`new_only`)**: Crawls only newly registered or unindexed domains and pages.
2. **Retry Failed (`retry_failed`)**: Automatically filters for websites with network timeouts, 5xx server errors, or transient rate limits with exponential backoff.
3. **Refresh Existing Data (`refresh_all`)**: Re-visits established manufacturer pages to detect updated phone extensions, executive changes, or relocations without creating duplicate records.

---

## Dashboard Views

1. **Overview Dashboard**: High-level KPI metric cards (Total Zones, Companies Discovered, Verified Contacts, Website Registry, Active Scraping Jobs), Bursa OSB directory status, and live execution telemetry.
2. **Industrial Zones Registry**: Comprehensive catalog of Bursa OSBs (Bursa OSB, DOSAB, NOSAB, Hasanağa OSB, Kayapa OSB, İnegöl OSB, TEKNOSAB, etc.) with official portal links and one-click scraping triggers.
3. **Companies Directory**: Searchable data grid filtering by zone, sector, and contact presence, displaying VKN tax numbers and contact badges.
4. **Public Business Contacts**: Professional email, phone, and department registry with confidence meter badges, copy-to-clipboard, verification toggles, and direct source URL provenance.
5. **Website Management**: Registry tracking domain status (`completed`, `in_progress`, `failed`, `pending`), crawl delay policies, robots.txt compliance status, and inline crawl mode switcher.
6. **Scraping History & Queue Tracker**: Asynchronous job monitor with real-time progress bars, success/failure counts, job cancellation, and collapsible telemetry log drawers.
7. **Excel Exports Center**: Multi-sheet workbook builder generating formatted `.xlsx` files with Companies, Contacts, Industrial Zones, Sources, and Scraping History sheets.

---

## Running with Docker Compose (Production / Full Stack)

1. Clone or copy the project files and create `.env`:
   ```bash
   cp .env.example .env
   ```

2. Start all services:
   ```bash
   docker compose up --build -d
   ```

3. Services will be available at:
   - **Frontend Dashboard**: [http://localhost:5173](http://localhost:5173) or [http://localhost:80](http://localhost:80)
   - **FastAPI Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Healthcheck**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
   - **PostgreSQL**: `localhost:5432`
   - **Redis**: `localhost:6379`

---

## Running Locally for Development

### Backend (FastAPI + SQLAlchemy)

```bash
# Navigate to backend and create virtualenv
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start FastAPI server with live reload
uvicorn app.main:app --reload --port 8000
```

### Frontend (React + Vite + Tailwind)

```bash
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
# Backend pytest test suite (100% passing)
python -m pytest backend/tests -v

# Frontend TypeScript verification
cd frontend
npm run typecheck
```

---

## Development Phases Roadmap

- [x] **Phase 1**: Architecture foundation, Docker Compose, normalized database schema, Alembic migrations, Bursa OSB initial seed, FastAPI REST API, and full React dashboard views.
- [ ] **Phase 2**: OSB and website registry automation (deep URL normalization, robots.txt parsers, adaptive crawl delay).
- [ ] **Phase 3**: Scraping engine and company discovery (HTTPX + BeautifulSoup directory scrapers, Playwright headless browser for dynamic portals).
- [ ] **Phase 4**: Contact extraction, confidence scoring, classification, and source provenance recording.
- [ ] **Phase 5**: Excel multi-sheet export generation (OpenPyXL), retry queues, automated refresh, and end-to-end integration tests.
- [ ] **Phase 6**: Security hardening, rate limiting, KVKK compliance audit, and production deployment.
# web_scraping
