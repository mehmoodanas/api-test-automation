"""
Project-wide pytest fixtures.

Fixtures here are visible to every test in `tests/` and `tests_ui/`.
We use session scope so the fixtures live for the whole test run —
this also avoids a ScopeMismatch with the pytest-base-url plugin
that ships with pytest-playwright.
"""
import pytest

from framework.api_client import APIClient


@pytest.fixture(scope="session")
def base_url():
    """The base URL of the API under test."""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_client(base_url):
    """A ready-to-use APIClient instance."""
    return APIClient(base_url)
