import time

from .models.asset import Asset
from .models.assets import Assets
from .models.market import Market
from .session import Session
from .parser import Parser
from .endpoints import API_PATH
from .listing import ListingGenerator
from .exceptions import TooManyRequests


class Messari:
    """Interface for interacting with the Messari API."""

    def __init__(self, session=None):
        self._session = session

        if self._session is None:
            self._session = self._initialize_session()

        self.parser = Parser(self)
        self.assets = Assets(self)

    def _initialize_session(self):
        return Session()

    def request(self, method, path, params=None):
        return self._session.request(method, path, params)

    def asset(self, id=None):
        return Asset(self, id=id)

    def markets(self, **generator_kwargs):
        return ListingGenerator(self, API_PATH["markets"], **generator_kwargs)

    def market(self, id=None):
        return Market(self, id=id)

    def news(self, **generator_kwargs):
        return ListingGenerator(self, API_PATH["news"], **generator_kwargs)
