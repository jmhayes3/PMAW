from .base import MessariBase


class Metrics(MessariBase):

    STR_FIELD = "id"
    PATH = "api/v1/assets/{asset}/metrics"

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
        metrics_data = data.json()["data"]
        metrics = type(self)(self._messari, _data=metrics_data)

        self.__dict__.update(metrics.__dict__)

        self._fetched = True
