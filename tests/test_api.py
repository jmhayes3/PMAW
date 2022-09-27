import time

import pytest

from requests import Session
from betamax import Betamax

from pmaw.messari import Messari
from pmaw.auth import Authenticator
from pmaw.listing import ListingGenerator
from pmaw.exceptions import BadRequest
from pmaw.models.asset import Asset


class IntegrationTest:
    def setup(self):
        self.messari = Messari()
        self.recorder = Betamax(self.messari._session.request_handler._session)


class TestMessariAPI(IntegrationTest):
    def test_session(self):
        session = self.messari._session.request_handler._session
        assert isinstance(session, Session)

    def test_assets(self):
        with self.recorder.use_cassette("test_assets"):
            assets = self.messari.assets.top()
            assert isinstance(assets, ListingGenerator)

            for asset in assets:
                assert isinstance(asset, Asset)

    def test_valid_api_key(self):
        with self.recorder.use_cassette("test_valid_api_key"):
            asset = self.messari.asset("ethereum").slug

    def test_invalid_api_key(self):
        auth = Authenticator("1")
        self.messari._session.request_handler._session.auth = auth
        with self.recorder.use_cassette("test_invalid_api_key"):
            with pytest.raises(BadRequest):
                asset = self.messari.asset("ethereum").slug
