from .models.asset import Asset
from .models.metrics import MarketData
from .util import flatten


class Parser:

    def __init__(self, messari):
        self._messari = messari

    def from_dict(self, data):
        if {"id", "slug", "symbol", "name"}.issubset(data):
           return Asset.from_data(self._messari, data)

        if {"price_usd"}.issubset(data):
            data = flatten(data)
            return MarketData.from_data(self._messari, data)

    def parse(self, data):
        if data is None:
            return None
        elif isinstance(data, list):
            return [self.parse(item) for item in data]
        elif isinstance(data, dict):
            return self.from_dict(data)
