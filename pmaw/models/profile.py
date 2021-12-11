from .base import MessariBase, PMAWBase
from ..endpoints import API_PATH


class Profile(MessariBase):
    """Asset profile."""

    def __init__(self, messari, id=None, _data=None, _fetched=False):
        if (id, _data).count(None) != 1:
            raise TypeError("Either `id` or `_data` required.")

        if id:
            self.id = id

        super().__init__(messari, _data=_data, _fetched=_fetched, _str_field=False)

    def __setattr__(self, attribute, value):
        if attribute == "general":
            pass
        super().__setattr__(attribute, value)

    def _fetch_data(self):
        path = API_PATH["asset_profile"].format(asset=self.id)
        params = {
            "as-markdown": "",
        }
        return self._messari.request("GET", path, params)

    def _fetch(self):
        data = self._fetch_data()
        profile_data = data.json()["data"]
        profile = type(self)(self._messari, _data=profile_data)

        for attribute, value in profile.profile.items():
            setattr(self, attribute, value)

        self._fetched = True


class ProfileOverview(PMAWBase):
    """Profile overview."""
