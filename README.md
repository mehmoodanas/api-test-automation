# API Test Automation Framework

[![Tests](https://github.com/mehmoodanas/api-test-automation/actions/workflows/tests.yml/badge.svg)](https://github.com/mehmoodanas/api-test-automation/actions/workflows/tests.yml)
[![Live Dashboard](https://img.shields.io/badge/Allure%20Report-live-blueviolet)](https://mehmoodanas.github.io/api-test-automation/)
[![Python](https://img.shields.io/badge/Python-3.13%2B-blue)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-9.x-brightgreen)](https://pytest.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.51-orange)](https://playwright.dev/)
[![Java](https://img.shields.io/badge/Java-21-red)](https://www.oracle.com/java/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A two-layer test automation framework demonstrating modern Python QA practices:
**REST API tests** with `requests` + `jsonschema`, and **end-to-end UI tests**
with Playwright using the **Page Object Model**. Containerised with Docker and
validated by GitHub Actions on every push.

## 📊 Live test dashboard

Every push to `main` triggers CI, runs the full suite, and **publishes a live Allure report** to GitHub Pages:

**👉 [View the live dashboard](https://mehmoodanas.github.io/api-test-automation/)**

The dashboard is interactive — drill into individual tests, see history across runs, view failures with stack traces, and inspect timing trends.

## Features

- **API tests** against [JSONPlaceholder](https://jsonplaceholder.typicode.com/)
  - Positive and negative cases (200, 201, 404)
  - JSON Schema validation of response bodies
  - Parametrised tests for multiple inputs
- **UI tests** against [Sauce Demo](https://www.saucedemo.com/)
  - Page Object Model (`LoginPage`, `InventoryPage`)
  - Successful login, locked-out user, wrong password
- **Reusable framework** layer (`framework/`)
  - `APIClient` wrapping `requests`
  - JSON Schemas in `framework/schemas.py`
  - Page Objects in `framework/pages/`
- **Pytest markers** for selective runs (`smoke`, `regression`, `negative`, `crud`, `ui`)
- **HTML test reports** via `pytest-html`
- **Docker** image based on Microsoft's official Playwright Python image
- **GitHub Actions CI** runs the suite on every push/PR

## Project structure

```
api-test-automation/
├── framework/
│   ├── api_client.py      # Reusable HTTP client
│   ├── schemas.py         # JSON Schemas
│   └── pages/             # Page Objects
│       ├── login_page.py
│       └── inventory_page.py
├── tests/                 # API tests
│   └── test_posts.py
├── tests_ui/              # Browser tests
│   └── test_login.py
├── .github/workflows/
│   └── tests.yml          # CI pipeline
├── conftest.py            # Project-wide fixtures
├── pytest.ini             # Pytest config & markers
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Run locally

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\activate.bat        # Windows
# source .venv/bin/activate          # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt
playwright install --with-deps chromium

# 3. Run all tests
pytest

# 4. Open the HTML report
start report.html                    # Windows
# open report.html                   # macOS
```

## Selective runs (using markers)

```bash
pytest -m smoke              # only smoke tests
pytest -m ui                 # only browser tests
pytest -m "smoke and not ui" # smoke API tests only
pytest -m negative           # only negative tests
pytest tests/                # only the API folder
pytest tests_ui/             # only the UI folder
```

## Run with Docker

```bash
docker compose build
docker compose up
```

The HTML report is written to `report.html` on the host (via the bind mount).

## Tech stack

| Layer | Tool |
|---|---|
| Language | Python 3.13+ |
| Test runner | Pytest 9 |
| HTTP client | `requests` |
| Schema validation | `jsonschema` |
| Browser automation | Playwright + `pytest-playwright` |
| Reporting | `pytest-html` (self-contained HTML) |
| Containerisation | Docker (Playwright Python image) |
| CI | GitHub Actions |

## What I learned building this

- Designing a layered test framework (`framework/` + `tests/` + `tests_ui/`)
- Pytest fixtures, parametrize, markers, and `conftest.py` scoping
- API contract testing via JSON Schema
- The Page Object Model pattern for UI test maintainability
- Containerisation and CI integration for a Python test suite

---

Built by Anas Mehmood as part of preparing for a test-automation internship.

---

## Java + RestAssured layer (bonus)

A parallel Java/RestAssured test suite under [`java-tests/`](java-tests/) mirrors
the Python tests against the same API. This proves the framework works in a
**unified Java + Python stack** — directly relevant to QA roles that require
both languages.

### Run the Java tests

```bash
cd java-tests
mvn test
```

Requires Java 21+ and Maven. RestAssured + JUnit 5 are pulled in via Maven on first run.

### What it covers

- `GET /posts/1` returns 200
- Response shape contains `id`, `title`, `body`, `userId`
- Parametrized GET over IDs 1–5
- Negative test: `GET /posts/9999` → 404
- `POST /posts` creates a resource and the API echoes the data back

---

## Performance & load testing (Locust)

Every API test asserts a **response-time threshold** (2 seconds) alongside its
status-code check. A separate Locust suite under [`performance/`](performance/)
runs heavier load scenarios: simulating multiple concurrent users hitting the
API, measuring throughput and percentile latency.

### Run the load test interactively

```bash
locust -f performance/locustfile.py --host https://jsonplaceholder.typicode.com
```

Open `http://localhost:8089`, set users + spawn-rate, click **Start swarming**,
and watch real-time charts of requests-per-second, response times, and failures.

### Run a headless smoke load test (same as CI)

```bash
locust -f performance/locustfile.py \
    --host https://jsonplaceholder.typicode.com \
    --users 5 --spawn-rate 1 --run-time 20s --headless
```

### What the suite covers

- **GET /posts/{id}** (weight 5 — most common)
- **GET /posts** (weight 3 — list)
- **POST /posts** (weight 1 — least common)

The mix is realistic — most users *read* far more than they *create*.


---

## Restful Booker layer (production-style API)

Beyond JSONPlaceholder, the suite also tests
[Restful Booker](https://restful-booker.herokuapp.com/) — a real, hosted booking
API that mirrors what production services look like:

- **Token-based authentication** (`POST /auth` returns a token used as a cookie)
- **Full CRUD** on `/booking` with validation
- **Realistic latency** from a hosted service
- **Real persistence** — create-then-read patterns are verifiable

### Test breakdown ([`tests/test_bookings.py`](tests/test_bookings.py))

- **Auth (2):** valid login returns a token; invalid login returns "Bad credentials"
- **Read (4):** list bookings, filter by lastname, get specific booking, 404 for missing
- **Create (2):** create + echo, then retrieve by id
- **Update (3):** PUT with token, PUT without token (403), PATCH partial update
- **Delete (3):** DELETE with token, DELETE without token (403), verify deletion via GET

Total: **14 additional tests** spanning happy paths, negative paths, and end-to-end persistence flows.
