from .models.asset import Asset

class Parser:

    def __init__(self, messari):
        self._messari = messari

    def from_dict(self, data):
        if {"id", "slug", "symbol", "name"}.issubset(data):
           return Asset.parse(self._messari, data)

    def to_object(self, data):
        if data is None:
            return None
        elif isinstance(data, list):
            return [self.to_object(item) for item in data]
        elif isinstance(data, dict):
            return self.from_dict(data)
