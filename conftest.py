"""
Project-wide pytest fixtures + Allure metadata setup.

Fixtures here are visible to every test in `tests/` and `tests_ui/`.
Session-scoped to live across the whole run and avoid ScopeMismatch
with the pytest-base-url plugin shipped with pytest-playwright.
"""
import json
import os
import shutil
from pathlib import Path

import pytest

from framework.api_client import APIClient


# --- Allure metadata setup ---------------------------------------------------

ALLURE_RESULTS_DIR = Path("allure-results")
ALLURE_META_DIR = Path("allure")


def pytest_configure(config):
    """
    Drop static metadata (environment.properties, categories.json) and a
    dynamic executor.json into allure-results/ so the Allure dashboard's
    Environment, Categories, and Executors panels are populated.

    Runs once at session start, before any tests collect.
    """
    ALLURE_RESULTS_DIR.mkdir(exist_ok=True)

    # Copy static files (environment + categories)
    for filename in ("environment.properties", "categories.json"):
        src = ALLURE_META_DIR / filename
        if src.exists():
            shutil.copy(src, ALLURE_RESULTS_DIR / filename)

    # Generate executor.json — CI vs local
    if os.getenv("GITHUB_ACTIONS") == "true":
        repo = os.getenv("GITHUB_REPOSITORY", "")
        run_id = os.getenv("GITHUB_RUN_ID", "")
        run_number = os.getenv("GITHUB_RUN_NUMBER", "")
        sha = os.getenv("GITHUB_SHA", "")[:7]
        branch = os.getenv("GITHUB_REF_NAME", "main")
        actor = os.getenv("GITHUB_ACTOR", "unknown")
        server = os.getenv("GITHUB_SERVER_URL", "https://github.com")

        executor = {
            "name": "GitHub Actions",
            "type": "github",
            "url": f"{server}/{repo}/actions/runs/{run_id}",
            "buildOrder": int(run_number) if run_number.isdigit() else 0,
            "buildName": f"#{run_number} on {branch} ({sha}) by @{actor}",
            "buildUrl": f"{server}/{repo}/actions/runs/{run_id}",
            "reportUrl": f"https://{repo.split('/')[0]}.github.io/{repo.split('/')[1]}/",
            "reportName": "Live Allure dashboard",
        }
    else:
        executor = {
            "name": "Local run",
            "type": "local",
            "buildName": "Developer machine (local pytest)",
        }

    (ALLURE_RESULTS_DIR / "executor.json").write_text(
        json.dumps(executor, indent=2)
    )


# --- JSONPlaceholder (basic CRUD without auth) -------------------------------

@pytest.fixture(scope="session")
def base_url():
    """Base URL of the JSONPlaceholder API."""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_client(base_url):
    """A ready-to-use APIClient pointing at JSONPlaceholder."""
    return APIClient(base_url)


# --- Restful Booker (production-style API with auth + CRUD) ------------------

BOOKER_USERNAME = "admin"
BOOKER_PASSWORD = "password123"


@pytest.fixture(scope="session")
def booker_base_url():
    """Base URL of the Restful Booker test API."""
    return "https://restful-booker.herokuapp.com"


@pytest.fixture(scope="session")
def booker_client(booker_base_url):
    """A ready-to-use APIClient pointing at Restful Booker."""
    return APIClient(booker_base_url)


@pytest.fixture(scope="session")
def booker_auth_token(booker_client):
    """Get a session-wide auth token for protected operations."""
    response = booker_client.post(
        "/auth",
        json={"username": BOOKER_USERNAME, "password": BOOKER_PASSWORD},
    )
    assert response.status_code == 200, (
        f"Failed to authenticate to Restful Booker: {response.text}"
    )
    token = response.json().get("token")
    assert token, f"No token returned from /auth: {response.json()}"
    return token


@pytest.fixture
def booker_auth_headers(booker_auth_token):
    """Cookie header carrying the auth token (Restful Booker convention)."""
    return {"Cookie": f"token={booker_auth_token}"}


@pytest.fixture
def created_booking(booker_client):
    """Create a fresh booking before the test and return (id, payload)."""
    payload = {
        "firstname": "Anas",
        "lastname": "Mehmood",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-06-01",
            "checkout": "2026-06-08",
        },
        "additionalneeds": "Breakfast",
    }
    response = booker_client.post("/booking", json=payload)
    assert response.status_code == 200, (
        f"Failed to seed booking: {response.text}"
    )
    booking_id = response.json()["bookingid"]
    return booking_id, payload
