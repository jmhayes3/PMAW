from .models.news import News
from .models.profile import General
from .models.metrics import MarketData
from .models.market import Market

from .models import asset


class Parser:

    def __init__(self, messari):
        self._messari = messari

    def from_dict(self, data):
        if {"slug", "symbol", "name"}.issubset(data):
            return asset.Asset.from_data(self._messari, data)

        if {"exchange_slug", "pair"}.issubset(data):
            return Market.from_data(self._messari, data)

        if {"title", "content", "author"}.issubset(data):
            return News.from_data(self._messari, data)

        if {"price_usd"}.issubset(data):
            return MarketData.from_data(self._messari, data)

        if {"overview", "roadmap", "background", "regulation"}.issubset(data):
            return General.from_data(self._messari, data)

    def parse(self, data):
        if data is None:
            return None
        elif isinstance(data, list):
            return [self.parse(item) for item in data]
        elif isinstance(data, dict):
            return self.from_dict(data)
