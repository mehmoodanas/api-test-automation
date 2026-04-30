"""
Tests for the /posts endpoint of JSONPlaceholder.

Every API test asserts both correctness AND that the endpoint responded
within a reasonable time (PERFORMANCE_THRESHOLD_SECONDS) — surfacing slow
endpoints alongside broken ones.
"""
import pytest
from jsonschema import validate

from framework.schemas import POST_SCHEMA

# Any single API call that takes longer than this is considered too slow
PERFORMANCE_THRESHOLD_SECONDS = 2.0


@pytest.mark.smoke
def test_get_single_post_returns_200(api_client):
    """Verify that fetching an existing post returns HTTP 200 quickly."""
    response = api_client.get("/posts/1")
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < PERFORMANCE_THRESHOLD_SECONDS


@pytest.mark.smoke
def test_get_post_response_matches_schema(api_client):
    """Verify the response body matches the POST_SCHEMA contract."""
    response = api_client.get("/posts/1")
    data = response.json()
    validate(instance=data, schema=POST_SCHEMA)
    assert data["id"] == 1
    assert response.elapsed.total_seconds() < PERFORMANCE_THRESHOLD_SECONDS


@pytest.mark.regression
@pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
def test_get_post_by_id_returns_200(api_client, post_id):
    """Verify multiple post IDs all return successfully and quickly."""
    response = api_client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["id"] == post_id
    assert response.elapsed.total_seconds() < PERFORMANCE_THRESHOLD_SECONDS


@pytest.mark.negative
def test_get_nonexistent_post_returns_404(api_client):
    """Negative test: requesting a post that doesn't exist returns 404 quickly."""
    response = api_client.get("/posts/9999")
    assert response.status_code == 404
    assert response.elapsed.total_seconds() < PERFORMANCE_THRESHOLD_SECONDS


@pytest.mark.smoke
@pytest.mark.crud
def test_create_post_returns_201_and_echoes_data(api_client):
    """POST creates a resource, echoes the data, and responds quickly."""
    new_post = {
        "title": "My first API test",
        "body": "I am learning automation",
        "userId": 1,
    }

    response = api_client.post("/posts", json=new_post)

    assert response.status_code == 201
    assert response.elapsed.total_seconds() < PERFORMANCE_THRESHOLD_SECONDS

    data = response.json()
    validate(instance=data, schema=POST_SCHEMA)
    assert data["title"] == new_post["title"]
    assert data["body"] == new_post["body"]
    assert data["userId"] == new_post["userId"]
    assert "id" in data
