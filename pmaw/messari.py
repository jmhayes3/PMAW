import time

from .models.asset import Asset
from .models.assets import Assets
from .session import Session
from .parser import Parser
from .endpoints import API_PATH
from .listing import ListingGenerator
from .exceptions import TooManyRequests

from . import log as logger


class Messari:

    def __init__(self, session=None, max_wait=60):
        self._session = session
        self._max_wait = max_wait

        if self._session is None:
            self._initialize_session()

        self.parser = Parser(self)

        self.assets = Assets(self)

    def _initialize_session(self):
        self._session = Session()

    def request(self, method, path, params=None):
        tries = 3
        while tries > 0:
            try:
                return self._session.request(method, path, params)
            except TooManyRequests as exception:
                logger.warning(exception)
                if exception.retry_after:
                    wait = float(exception.retry_after) + 1
                    if wait > self._max_wait:
                        logger.info("Max wait exceeded")
                        continue
                    else:
                        logger.info(f"Sleeping {wait} seconds")
                        time.sleep(wait)
            finally:
                tries -= 1

    def asset(self, id=None):
        return Asset(self, id=id)

    def news(self, **generator_kwargs):
        return ListingGenerator(self, API_PATH["news"], **generator_kwargs)

    def markets(self, **generator_kwargs):
        return ListingGenerator(self, API_PATH["markets"], **generator_kwargs)
