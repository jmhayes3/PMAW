from .base import MessariBase
from .metrics import Metrics
from .profile import Profile
from ..endpoints import API_PATH
from ..timeseries import TimeseriesGenerator
from ..listing import ListingGenerator
from ..cache import cached_property


class Asset(MessariBase):

    def __init__(self, messari, id=None, _data=None, _fetched=False):
        if (id, _data).count(None) != 1:
            raise ValueError("Either `id` or `_data` required.")

        if id:
            self.id = id

        super().__init__(messari, _data=_data, _fetched=_fetched)

    def _fetch(self):
        data = self._messari.request("GET", self._path).json()["data"]
        asset = type(self)(self._messari, _data=data)

        self.__dict__.update(asset.__dict__)

        self._fetched = True

    @cached_property
    def metrics(self):
        return Metrics(self)

    @cached_property
    def profile(self):
        return Profile(self)

    def timeseries(self, metric, start, end, interval="1d", limit=None):
        path = API_PATH["asset_metric_time_series"].format(
            asset=self.id,
            metric=metric,
        )
        params = dict(start=start, end=end, interval=interval)
        return TimeseriesGenerator(self._messari, path, params, limit)

    def news(self, **generator_kwargs):
        return ListingGenerator(
            self._messari,
            API_PATH["asset_news"].format(asset=self.id),
            **generator_kwargs
        )

    @property
    def _path(self):
        return API_PATH["asset"].format(asset=self.id)
