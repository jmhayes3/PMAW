from copy import deepcopy

from .models.base import PMAWBase
from .exceptions import NotFound


class ListingGenerator(PMAWBase):

    def __init__(self, messari, path, limit=500, params=None):
        super().__init__(messari, _data=None)

        self.exhausted = False
        self.batch = None
        self.batch_index = None
        self.yielded = 0

        self.path = path
        self.limit = limit
        self.params = {}

        if params:
            self.params = deepcopy(params)

        self.params["limit"] = limit or 500
        self.params["page"] = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit is not None and self.yielded >= self.limit:
            raise StopIteration

        if self.batch is None or self.batch_index >= len(self.batch):
            if self.exhausted:
                raise StopIteration

            try:
                batch = self._messari.request(
                    "GET",
                    self.path,
                    self.params
                ).json()["data"]
                batch = self._messari.parser.parse(batch)
                if batch and isinstance(batch, list):
                    self.batch = batch
                else:
                    raise StopIteration
            except NotFound:
                raise StopIteration

            if len(self.batch) < self.params["limit"]:
                self.exhausted = True

            self.batch_index = 0
            self.params["page"] += 1

        self.batch_index += 1
        self.yielded += 1

        return self.batch[self.batch_index - 1]
