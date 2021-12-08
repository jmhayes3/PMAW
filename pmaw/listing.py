from copy import deepcopy

from .models.base import PMAWBase


class ListingGenerator(PMAWBase):

    def __init__(self, messari, url, page, limit=20, params=None):
        super().__init__(messari, _data=None)

        self._exhausted = False
        self._listing = None
        self._list_index = None

        self.url = url
        self.page = page
        self.limit = limit
        self.params = params

        if self.params:
            self.params = deepcopy(params)
        else:
            self.params = {}

        self.params["limit"] = limit or 500

        self.yielded = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit is not None and self.yielded >= self.limit:
            raise StopIteration

        if self._listing is None or self._list_index >= len(self._listing):
            self._next_batch()

        self._list_index += 1
        self.yielded += 1

        return self._listing[self._list_index - 1]

    def _next_batch(self):
        if self._exhausted:
            raise StopIteration

        self._listing = self._messari.request("GET", self.url, self.params)

        if isinstance(self._listing, list):
            self._listing = self._listing[1]
        elif isinstance(self._listing, dict):
            break
        self._list_index = 0

        if not self._listing:
            raise StopIteration

        if self._listing.after and self._listing.after != self.params.get("after"):
            self.params["after"] = self._listing.after
        else:
            self._exhausted = True
