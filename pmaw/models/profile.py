from .base import PMAWBase
from ..util import flatten


class Profile(PMAWBase):

    PATH = "api/v2/assets/{asset}/profile"

    def __init__(self, messari, id=None, _data=None):
        if (id, _data).count(None) != 1:
            raise TypeError("Either `id` or `_data` required.")

        if id:
            self.id = id

        super().__init__(messari, _data=_data)

        self._path = self.PATH.format(asset=self)
        self._params = {
            "as-markdown": "",
        }
        # self._params = {}

    def __setattr__(self, attribute, value):
        # if attribute == "general":
        #     value = General()

        super().__setattr__(attribute, value)

    def _fetch_data(self):
        return self._messari.request("GET", self._path, self._params)

    def _fetch(self):
        data = self._fetch_data()
        profile_data = data.json()["data"]
        profile = type(self)(self._messari, _data=profile_data)

        self.__dict__.update(profile.__dict__)

        for attribute, value in profile.profile.items():
            setattr(self, attribute, value)

        delattr(self, "profile")

        self._fetched = True
