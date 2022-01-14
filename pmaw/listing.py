from copy import deepcopy
from urllib.parse import urljoin

from .models.base import PMAWBase
from .endpoints import API_PATH
from .exceptions import NotFound


class ListingGenerator(PMAWBase):

    def __init__(self, messari, path, limit=500, params=None):
        super().__init__(messari, _data=None)

        self._exhausted = False
        self._listing = None
        self._list_index = None

        self.path = path
        self.limit = limit
        self.params = params

        if self.params:
            self.params = deepcopy(params)
        else:
            self.params = {}

        self.params["limit"] = limit or 500
        self.params["page"] = 1

        self.yielded = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit is not None and self.yielded >= self.limit:
            raise StopIteration

        if self._listing is None or self._list_index >= len(self._listing):
            if self._exhausted:
                raise StopIteration

            try:
                response = self._messari.request("GET", self.path, self.params).json()
                if {"status", "data"}.issubset(response):
                    data = response["data"]
                    self._listing = self._messari.parser.parse(data)
            except NotFound:
                raise StopIteration

            if not isinstance(self._listing, list):
                raise StopIteration

            if len(self._listing) < self.params["limit"]:
                self._exhausted = True

            self._list_index = 0
            self.params["page"] += 1

        self._list_index += 1
        self.yielded += 1

        return self._listing[self._list_index - 1]
