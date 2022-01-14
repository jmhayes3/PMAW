import time

from copy import deepcopy
from urllib.parse import urljoin
from datetime import datetime, timedelta

from .models.base import PMAWBase
from .endpoints import API_PATH
from .exceptions import NotFound

from . import log as logger


class MarketTimeseries(PMAWBase):
    """Market time series helper."""

    def __init__(self, market):
        super().__init__(market._messari, _data=None)

        self.market = market

    def __call__(self, metric_id, **generator_kwargs):
        return TimeseriesGenerator(
            self._messari,
            API_PATH["market_metric_time_series"].format(
                asset=self.market.id,
                metric_id=metric_id
            ),
            **generator_kwargs
        )


class AssetTimeseries(PMAWBase):
    """Asset time series helper."""

    def __init__(self, asset):
        super().__init__(asset._messari, _data=None)

        self.asset = asset

    def __call__(self, metric_id, start, end, interval="1d", **generator_kwargs):
        return TimeseriesGenerator(
            self._messari,
            API_PATH["asset_metric_time_series"].format(
                asset=self.asset.id,
                metric_id=metric_id
            ),
            start,
            end,
            interval,
            **generator_kwargs
        )


class TimeseriesGenerator(PMAWBase):
    """Time series generator."""

    INTERVALS = {
        "1m": 60,
        "5m": 300,
        "15m": 900,
        "30m": 1800,
        "1h": 3600,
        "1d": 86400,
        "1w": 604800,
    }

    def get_offset(self, start, end, interval="1d", max_points=2016):
        if not all((start, end)):
            raise ValueError("Both `start` and `end` are required.")
        elif interval not in self.INTERVALS:
            raise ValueError("Invalid interval.")

        if isinstance(start, str):
            start = datetime.fromisoformat(start)
        elif isinstance(end, str):
            end = datetime.fromisoformat(end)

        start_dt = start
        logger.info(f"Start datetime: {start_dt}")

        end_dt = end
        logger.info(f"End datetime: {end_dt}")

        if start_dt == end_dt:
            return None

        time_delta = end_dt - start_dt
        logger.info(f"Timedelta: {time_delta}")
        if time_delta.days < 0:
            return None

        interval_offset = self.INTERVALS[interval] * max_points
        logger.info(f"Interval offset: {interval_offset}")

        next_dt = start_dt + timedelta(seconds=interval_offset)
        logger.info(f"Next datetime: {next_dt}")

        next_dt = min(next_dt, end_dt)

        return next_dt.isoformat()

    def __init__(self, messari, path, start, end, interval="1d", limit=2016, params=None):
        super().__init__(messari, _data=None)

        self._batch = None
        self._batch_index = None
        self._batch_size = 2016

        self.path = path
        self.start = datetime.fromisoformat(start)
        self.end = datetime.fromisoformat(end)
        self.interval = interval
        self.limit = limit
        self.timestamp_format = "rfc3339"

        self.params = deepcopy(params) if params else {}

        self.params["timestamp-format"] = self.timestamp_format
        self.params["interval"] = self.interval

        self.params["start"] = self.start.isoformat()
        self.params["end"] = self.get_offset(self.start, self.end)

        self.exhausted = False

        self.yielded = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit is not None and self.yielded >= self.limit:
            raise StopIteration

        if self._batch is None or self._batch_index >= len(self._batch):
            if self.exhausted:
                raise StopIteration

            response = self._messari.request("GET", self.path, self.params)
            self._batch = response.json()["data"]["values"]
            if not self._batch or not isinstance(self._batch, list):
                raise StopIteration

            # datetimes are inclusive so add `interval` seconds to start date
            self.params["start"] = self.params["end"]
            start = datetime.fromisoformat(self.params["start"])
            delta = timedelta(seconds=self.INTERVALS[self.interval])
            self.params["start"] = (start + delta).isoformat()

            offset = self.get_offset(self.params["start"], self.end)
            if offset is None:
                self.exhausted = True
            else:
                self.params["end"] = offset

            self._batch_index = 0

        self._batch_index += 1
        self.yielded += 1

        return self._batch[self._batch_index - 1]
