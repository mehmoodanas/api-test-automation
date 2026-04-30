"""
APIClient — a thin wrapper around the `requests` library.

Holds a base URL and exposes simple get/post/put/patch/delete methods
so tests don't have to repeat the URL or HTTP details everywhere.
Supports optional headers for authenticated requests.
"""
import requests


class APIClient:
    """HTTP client for the API under test."""

    def __init__(self, base_url):
        """Store the base URL when a new client is created."""
        self.base_url = base_url

    def get(self, path, headers=None, params=None):
        """Send a GET request to base_url + path."""
        return requests.get(
            f"{self.base_url}{path}", headers=headers, params=params
        )

    def post(self, path, json=None, headers=None):
        """Send a POST request with a JSON body."""
        return requests.post(
            f"{self.base_url}{path}", json=json, headers=headers
        )

    def put(self, path, json=None, headers=None):
        """Send a PUT request with a JSON body."""
        return requests.put(
            f"{self.base_url}{path}", json=json, headers=headers
        )

    def patch(self, path, json=None, headers=None):
        """Send a PATCH request with a JSON body (partial update)."""
        return requests.patch(
            f"{self.base_url}{path}", json=json, headers=headers
        )

    def delete(self, path, headers=None):
        """Send a DELETE request."""
        return requests.delete(f"{self.base_url}{path}", headers=headers)
