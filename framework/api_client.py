"""
APIClient - a thin wrapper around the 'requests' library.

it holds the base URL and exposes simple get/post/put/delete methods
so test dont have to repeat the URL or HTTP details everywhere.
"""

import requests
class APIClient:
    """ HTTP client for the API under test. """

    def __init__(self, base_url):
        """ # Store the base URL when a new client is created. """
        self.base_url = base_url

    def get(self, path):
        """Send a GET request to bse_url + path"""
        return requests.get(f"{self.base_url}{path}")
    
    def post(self, path, json):
        """Send a Post request with a JSON body"""
        return requests.post(f"{self.base_url}{path}", json=json)
    
    def put(self, path, json):
        """Send a PUT request with a JSON body"""
        return requests.put(f"{self. base_url}{path}", json=json)
    
    def delete(self, path):
        """Send a DELETE request"""
        return requests.delete(f"{self.base_url}{path}")
    
