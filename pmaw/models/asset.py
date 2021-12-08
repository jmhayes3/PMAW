from .base import MessariBase
from .metrics import Metrics
from .profile import Profile


class Asset(MessariBase):

    STR_FIELD = "id"
    PATH = "api/v1/assets/{asset}"

    def __init__(self, messari, id=None, _data=None):
        if (id, _data).count(None) != 1:
            raise TypeError("Either `id` or `_data` required.")

        if id:
            self.id = id

        super().__init__(messari, _data=_data)

        self._path = self.PATH.format(asset=self)
        self._params = {}

    def __setattr__(self, attribute, value):
        super().__setattr__(attribute, value)

    def _fetch_data(self):
        return self._messari.request("GET", self._path, self._params)

    def _fetch(self):
        data = self._fetch_data()
        asset_data = data.json()["data"]
        asset = type(self)(self._messari, _data=asset_data)

        self.__dict__.update(asset.__dict__)

        self._fetched = True

    @property
    def metrics(self):
        return Metrics(self._messari, id=self.id)

    @property
    def profile(self):
        return Profile(self._messari, id=self.id)

    @property
    def news(self):
        return None
