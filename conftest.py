"""
Project-wide pytest fixtures.

Fixtures here are visible to every test in `tests/` and `tests_ui/`.
Session-scoped to live across the whole run and avoid ScopeMismatch
with the pytest-base-url plugin shipped with pytest-playwright.
"""
import pytest

from framework.api_client import APIClient


# --- JSONPlaceholder (basic CRUD without auth) ---

@pytest.fixture(scope="session")
def base_url():
    """Base URL of the JSONPlaceholder API."""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_client(base_url):
    """A ready-to-use APIClient pointing at JSONPlaceholder."""
    return APIClient(base_url)


# --- Restful Booker (production-style API with auth + CRUD) ---

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
    """
    Get a session-wide auth token for protected operations.

    Uses the documented test credentials. Token is valid for the
    duration of the test session.
    """
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
    """
    Create a fresh booking before the test and return (id, payload).
    Each test that needs a real booking gets its own.
    """
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
