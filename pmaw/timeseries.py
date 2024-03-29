from copy import deepcopy
from datetime import datetime, timedelta

from .models.base import PMAWBase
from .endpoints import API_PATH


def format_timestamp(timestamp):
    return timestamp.rstrip("Z")


class TimeseriesGenerator(PMAWBase):
    """Time series generator."""

    MAX_BATCH_SIZE = 2016

    VALID_INTERVALS = {
        "1m": 60,
        "5m": 300,
        "15m": 900,
        "30m": 1800,
        "1h": 3600,
        "1d": 86400,
        "1w": 604800,
    }

    @property
    def interval_seconds(self):
        return self.VALID_INTERVALS[self.interval]

    @property
    def max_interval_seconds(self):
        return self.interval_seconds * self.MAX_BATCH_SIZE

    def get_batch_interval(self, start, end, offset=False):
        if (start, end).count(None) != 0:
            raise ValueError("Both `start` and `end` are required.")

        start = datetime.fromisoformat(start)
        end = datetime.fromisoformat(end)

        # dates are inclusive, increment by `interval` if not the first batch
        if offset:
            start = start + timedelta(seconds=self.interval_seconds)

        batch_end = start + timedelta(seconds=self.max_interval_seconds)
        end = min(batch_end, end)

        return start, end

    def __init__(self, messari, path, params, limit=None):
        super().__init__(messari, _data=None)

        self.batch = None
        self.batch_index = None
        self.batch_num = 0
        self.yielded = 0
        self.exhausted = False

        self.path = path
        self.params = deepcopy(params)
        self.limit = limit

        self.start = self.params["start"]
        self.end = self.params["end"]
        self.interval = self.params["interval"]

        if self.interval not in self.VALID_INTERVALS:
            raise ValueError("Invalid interval.")

        self.params["timestamp-format"] = "rfc3339"

        start, end = self.get_batch_interval(self.start, self.end)
        self.params["start"] = start.isoformat()
        self.params["end"] = end.isoformat()

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit is not None and self.yielded >= self.limit:
            raise StopIteration

        if self.batch is None or self.batch_index >= len(self.batch):
            if self.exhausted:
                raise StopIteration

            batch = self._messari.request(
                "GET",
                self.path,
                self.params
            ).json()["data"]["values"]

            if batch and isinstance(batch, list):
                self.batch = batch
            else:
                raise StopIteration

            start, end = self.get_batch_interval(
                self.params["end"],
                self.end,
                offset=True
            )

            if start >= end:
                self.exhausted = True

            self.params["start"] = start.isoformat()
            self.params["end"] = end.isoformat()

            end_timestamp = format_timestamp(self.batch[-1][0])
            if end_timestamp == self.params["end"]:
                self.exhausted = True

            self.batch_num += 1
            self.batch_index = 0

        self.batch_index += 1
        self.yielded += 1

        return self.batch[self.batch_index - 1]
