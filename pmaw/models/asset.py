from .base import MessariBase
from .metrics import Metrics
from .profile import Profile
from ..endpoints import API_PATH
from ..listing import NewsListingMixin


class Asset(NewsListingMixin, MessariBase):

    def __init__(self, messari, id=None, _data=None):
        if (id, _data).count(None) != 1:
            raise TypeError("Either `id` or `_data` required.")

        if id:
            self.id = id

        self._metrics = None
        self._profile = None

        super().__init__(messari, _data=_data)

    def __setattr__(self, attribute, value):
        if attribute == "metrics":
            self._metrics = Metrics(self._messari, _data=value)
        elif attribute == "profile":
            self._profile = Profile(self._messari, _data=value)
        super().__setattr__(attribute, value)

    def __getattr__(self, attribute):
        if attribute == "metrics":
            if self._metrics is None:
                self._metrics = Metrics(self._messari, id=self.id)
            return self._metrics
        elif attribute == "profile":
            if self._profile is None:
                self._profile = Profile(self._messari, id=self.id)
            return self._profile

    def _fetch_data(self):
        return self._messari.request("GET", self._path, params=None)

    def _fetch(self):
        data = self._fetch_data()
        asset_data = data.json()["data"]
        asset = type(self)(self._messari, _data=asset_data)

        self.__dict__.update(asset.__dict__)

        self._fetched = True

    @property
    def _path(self):
        return API_PATH["asset"].format(asset=self.id)
