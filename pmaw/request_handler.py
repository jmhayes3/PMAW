import requests

from .exceptions import RequestException


class RequestHandler:

    def __init__(self, auth=None, session=None):
        self._session = session or requests.Session()

        if auth:
            self._session.auth = auth

    def close(self):
        return self._session.close()

    def request(self, *args, **kwargs):
        try:
            return self._session.request(*args, **kwargs)
        except Exception as e:
            raise RequestException(e, args, kwargs)
