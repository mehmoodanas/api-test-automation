# API Test Automation Framework

[![Tests](https://github.com/mehmoodanas/api-test-automation/actions/workflows/tests.yml/badge.svg)](https://github.com/mehmoodanas/api-test-automation/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.13%2B-blue)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-9.x-brightgreen)](https://pytest.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.51-orange)](https://playwright.dev/)

A two-layer test automation framework demonstrating modern Python QA practices:
**REST API tests** with `requests` + `jsonschema`, and **end-to-end UI tests**
with Playwright using the **Page Object Model**. Containerised with Docker and
validated by GitHub Actions on every push.

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
