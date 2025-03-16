from enum import Enum
import requests


class HttpMethods(Enum):
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PATCH = 'PATCH'


class ApiClient:

    def __init__(self, base_url: str):
        self.url = base_url

    def _create_url(self, endpoint):
        return f'{self.url}/{endpoint}'

    def send_request(self, method: HttpMethods, endpoint: str, **kwargs):
        url = self._create_url(endpoint)
        return requests.request(method.value, url, **kwargs)
