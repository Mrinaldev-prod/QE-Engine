import requests


class APIClient:
    def __init__(self, base_url: str):
        self.base = base_url.rstrip('/')

    def login(self, email: str, password: str):
        return requests.post(f"{self.base}/api/login", json={"email": email, "password": password})
