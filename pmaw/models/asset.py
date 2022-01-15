from .base import MessariBase
from .metrics import Metrics
from .profile import Profile
from .news import News
from ..endpoints import API_PATH
from ..timeseries import AssetTimeseries


class Asset(MessariBase):

    def __init__(self, messari, id=None, _data=None, _fetched=False):
        if (id, _data).count(None) != 1:
            raise TypeError("Either `id` or `_data` required.")

        if id:
            self.id = id

        super().__init__(messari, _data=_data, _fetched=_fetched)

        self.metrics = Metrics(self, None)
        self.profile = Profile(self, None)
        self.news = News(self)
        self.timeseries = AssetTimeseries(self)

    def __setattr__(self, attribute, value):
        super().__setattr__(attribute, value)

    def _fetch_data(self):
        return self._messari.request("GET", self._path, params=None)

    def _fetch(self):
        data = self._fetch_data().json()["data"]
        asset = type(self)(self._messari, _data=data)

        self.__dict__.update(asset.__dict__)

        self._fetched = True

    @property
    def _path(self):
        return API_PATH["asset"].format(asset=self.id)
