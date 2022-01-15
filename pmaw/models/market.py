from .base import PMAWBase
from ..endpoints import API_PATH
from ..timeseries import TimeseriesGenerator


class Market(PMAWBase):
    """Market data."""

    def __init__(self, messari, id=None, _data=None):
        if (id, _data).count(None) != 1:
            raise TypeError("Either `id` or `_data` required.")

        if id:
            self.id = id

        super().__init__(messari, _data=_data)

    def timeseries(self, metric, start, end, interval="1d", limit=None):
        path = API_PATH["market_metric_time_series"].format(
            market=self.id,
            metric=metric
        )
        params = dict(start=start, end=end, interval=interval)
        return TimeseriesGenerator(self._messari, path, params, limit)
