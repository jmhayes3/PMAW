import os

from .models.asset import Asset
from .models.assets import Assets
from .models.market import Market
from .session import Session
from .auth import Authenticator
from .request_handler import RequestHandler
from .rate_limiter import RateLimiter
from .parser import Parser
from .endpoints import API_PATH
from .listing import ListingGenerator
from .exceptions import TooManyRequests


class Messari:
    """Interface for interacting with the Messari API."""

    def __init__(self, api_key=None, target_rate=None, session=None):
        self.api_key = api_key
        self.target_rate = target_rate
        self._session = session

        if not self.api_key:
            self.api_key = os.environ.get("X_MESSARI_API_KEY")

        if self._session is None:
            self._session = self._initialize_session()

        self.parser = Parser(self)
        self.assets = Assets(self)

    def _initialize_session(self):
        auth = Authenticator(self.api_key)
        request_handler = RequestHandler(auth=auth)

        rate_limiter = RateLimiter()

        if self.target_rate:
            rate_limiter.target_rate = self.target_rate

        return Session(request_handler, rate_limiter)

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
