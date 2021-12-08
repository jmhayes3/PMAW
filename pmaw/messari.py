from .models.asset import Asset
from .session import Session


class Messari:

    def __init__(self, session=None):
        self._session = session

        if self._session is None:
            self._initialize_session()

    def _initialize_session(self):
        self._session = Session()

    def request(self, method, path, params=None):
        try:
            return self._session.request(method, path, params)
        except Exception as e:
            raise e

    def asset(self, id=None):
        return Asset(self, id=id)
