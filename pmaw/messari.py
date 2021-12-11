from .models.asset import Asset
from .models.assets import Assets
from .session import Session
from .parser import Parser


class Messari:

    def __init__(self, session=None):
        self._session = session

        if self._session is None:
            self._initialize_session()

        self.parser = Parser(self)

        self.assets = Assets(self)

    def _initialize_session(self):
        self._session = Session()

    def request(self, method, path, params=None):
        return self._session.request(method, path, params)

    def asset(self, id=None):
        return Asset(self, id=id)
