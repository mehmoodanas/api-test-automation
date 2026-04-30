"""
End-to-end tests for the Restful Booker API.

A more production-style API than JSONPlaceholder:
- Token-based authentication required for write operations.
- Full CRUD over /booking.
- Real persistence (create-then-read patterns are verifiable).
- Realistic latency from a hosted service.

We cover positive, negative, and authentication scenarios — the same
shape of suite a junior QA would inherit on day one.
"""
import pytest
from jsonschema import validate

from framework.schemas import (
    AUTH_TOKEN_SCHEMA,
    BOOKING_SCHEMA,
    CREATE_BOOKING_RESPONSE_SCHEMA,
)

# Hosted service may be slower than JSONPlaceholder; use a generous threshold
PERFORMANCE_THRESHOLD_SECONDS = 10.0


# ============================================================
# AUTH
# ============================================================

@pytest.mark.smoke
def test_create_token_returns_token_for_valid_credentials(booker_client):
    """POST /auth returns a non-empty token for the documented test credentials."""
    response = booker_client.post(
        "/auth",
        json={"username": "admin", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    validate(instance=data, schema=AUTH_TOKEN_SCHEMA)


@pytest.mark.negative
def test_create_token_with_invalid_credentials_returns_reason(booker_client):
    """POST /auth with bad credentials returns 200 + a 'reason' field
    instead of a token (Restful Booker convention)."""
    response = booker_client.post(
        "/auth",
        json={"username": "admin", "password": "DEFINITELY_WRONG"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" not in data
    assert data.get("reason") == "Bad credentials"


# ============================================================
# READ — list & single booking
# ============================================================

@pytest.mark.smoke
def test_list_bookings_returns_array_of_ids(booker_client):
    """GET /booking returns a list of {bookingid:int} objects."""
    response = booker_client.get("/booking")
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < PERFORMANCE_THRESHOLD_SECONDS

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for item in data[:5]:
        assert "bookingid" in item
        assert isinstance(item["bookingid"], int)


@pytest.mark.smoke
def test_get_specific_booking_matches_schema(booker_client, created_booking):
    """GET /booking/{id} returns a valid booking object matching the schema."""
    booking_id, _ = created_booking
    response = booker_client.get(f"/booking/{booking_id}")
    assert response.status_code == 200
    data = response.json()
    validate(instance=data, schema=BOOKING_SCHEMA)


@pytest.mark.regression
def test_filter_bookings_by_lastname(booker_client, created_booking):
    """GET /booking?lastname=Mehmood returns at least the booking we just made."""
    _, payload = created_booking
    response = booker_client.get(
        "/booking", params={"lastname": payload["lastname"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.negative
def test_get_nonexistent_booking_returns_404(booker_client):
    """GET /booking/{huge_id} returns 404 for a booking that doesn't exist."""
    response = booker_client.get("/booking/99999999")
    assert response.status_code == 404


# ============================================================
# CREATE
# ============================================================

@pytest.mark.smoke
@pytest.mark.crud
def test_create_booking_returns_id_and_echoes_data(booker_client):
    """POST /booking returns 200 with a new bookingid and echoes the payload."""
    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 199,
        "depositpaid": False,
        "bookingdates": {"checkin": "2026-07-01", "checkout": "2026-07-05"},
        "additionalneeds": "Late checkout",
    }
    response = booker_client.post("/booking", json=payload)
    assert response.status_code == 200

    data = response.json()
    validate(instance=data, schema=CREATE_BOOKING_RESPONSE_SCHEMA)
    assert data["booking"]["firstname"] == payload["firstname"]
    assert data["booking"]["lastname"] == payload["lastname"]
    assert data["booking"]["totalprice"] == payload["totalprice"]


@pytest.mark.crud
def test_created_booking_can_be_fetched(booker_client, created_booking):
    """A booking we just created should be retrievable by id."""
    booking_id, payload = created_booking
    response = booker_client.get(f"/booking/{booking_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["firstname"] == payload["firstname"]
    assert data["lastname"] == payload["lastname"]


# ============================================================
# UPDATE — requires auth
# ============================================================

@pytest.mark.crud
def test_update_booking_with_token_returns_200(
    booker_client, booker_auth_headers, created_booking
):
    """PUT /booking/{id} with a valid token returns 200 and the updated booking."""
    booking_id, _ = created_booking
    updated = {
        "firstname": "Anas",
        "lastname": "Updated",
        "totalprice": 999,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-08-01", "checkout": "2026-08-10"},
        "additionalneeds": "Vegan menu",
    }
    response = booker_client.put(
        f"/booking/{booking_id}", json=updated, headers=booker_auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["lastname"] == "Updated"
    assert data["totalprice"] == 999


@pytest.mark.negative
def test_update_booking_without_token_returns_403(booker_client, created_booking):
    """PUT /booking/{id} without auth returns 403 Forbidden."""
    booking_id, _ = created_booking
    payload = {
        "firstname": "Should",
        "lastname": "Fail",
        "totalprice": 1,
        "depositpaid": False,
        "bookingdates": {"checkin": "2026-09-01", "checkout": "2026-09-02"},
    }
    response = booker_client.put(f"/booking/{booking_id}", json=payload)
    assert response.status_code == 403


@pytest.mark.crud
def test_partial_update_booking_with_token_returns_200(
    booker_client, booker_auth_headers, created_booking
):
    """PATCH /booking/{id} with a valid token applies only the changed fields."""
    booking_id, original = created_booking
    response = booker_client.patch(
        f"/booking/{booking_id}",
        json={"firstname": "Patched"},
        headers=booker_auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["firstname"] == "Patched"
    # Other fields preserved
    assert data["lastname"] == original["lastname"]


# ============================================================
# DELETE — requires auth
# ============================================================

@pytest.mark.crud
def test_delete_booking_with_token_returns_201(
    booker_client, booker_auth_headers, created_booking
):
    """DELETE /booking/{id} with a valid token returns 201 Created (Booker convention)."""
    booking_id, _ = created_booking
    response = booker_client.delete(
        f"/booking/{booking_id}", headers=booker_auth_headers
    )
    assert response.status_code == 201


@pytest.mark.negative
def test_delete_booking_without_token_returns_403(booker_client, created_booking):
    """DELETE /booking/{id} without a token returns 403 Forbidden."""
    booking_id, _ = created_booking
    response = booker_client.delete(f"/booking/{booking_id}")
    assert response.status_code == 403


@pytest.mark.crud
def test_deleted_booking_then_get_returns_404(
    booker_client, booker_auth_headers, created_booking
):
    """After deletion, a GET on the same id must return 404."""
    booking_id, _ = created_booking
    delete_response = booker_client.delete(
        f"/booking/{booking_id}", headers=booker_auth_headers
    )
    assert delete_response.status_code == 201

    get_response = booker_client.get(f"/booking/{booking_id}")
    assert get_response.status_code == 404
