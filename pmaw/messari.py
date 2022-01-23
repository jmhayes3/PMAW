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

    def __init__(self, session=None, max_wait=60):
        self._session = session

        if self._session is None:
            self._session = self._initialize_session()

        self.max_wait = max_wait

        self.parser = Parser(self)
        self.assets = Assets(self)

    def _initialize_session(self):
        return Session()

    def request(self, method, path, params=None):
        tries = 3
        while tries > 0:
            try:
                return self._session.request(method, path, params)
            except TooManyRequests as exception:
                if exception.retry_after:
                    wait = float(exception.retry_after) + 1
                    if wait > self.max_wait:
                        break
                    else:
                        time.sleep(wait)
            finally:
                tries -= 1

    def asset(self, id=None):
        return Asset(self, id=id)

    def markets(self, **generator_kwargs):
        return ListingGenerator(self, API_PATH["markets"], **generator_kwargs)

    def market(self, id=None):
        return Market(self, id=id)

    def news(self, **generator_kwargs):
        return ListingGenerator(self, API_PATH["news"], **generator_kwargs)
