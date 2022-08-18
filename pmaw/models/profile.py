from .base import MessariBase, PMAWBase, PMAWList
from ..endpoints import API_PATH

from . import asset


class Profile(MessariBase):
    """Asset profile."""

    def __init__(self, asset, _data=None):
        super().__init__(asset._messari, _data=_data)

        self.asset = asset

    def __setattr__(self, attribute, value):
        if attribute == "general":
            value = General.from_data(self._messari, value)
        elif attribute == "contributors":
            value = Contributors.from_data(self._messari, value)
        elif attribute == "advisors":
            value = Advisors.from_data(self._messari, value)
        elif attribute == "investors":
            value = Investors.from_data(self._messari, value)
        elif attribute == "ecosystem":
            value = Ecosystem.from_data(self._messari, value)
        elif attribute == "economics":
            value = Economics.from_data(self._messari, value)
        elif attribute == "technology":
            value = Technology.from_data(self._messari, value)
        elif attribute == "governance":
            value = Governance.from_data(self._messari, value)
        super().__setattr__(attribute, value)

    def _fetch(self):
        path = API_PATH["asset_profile"].format(asset=self.asset.id)
        params = {}
        data = self._messari.request("GET", path, params).json()["data"]
        data = data.pop("profile") if "profile" in data else data
        profile = type(self)(self.asset, _data=data)

        self.__dict__.update(profile.__dict__)
        self._fetched = True



class General(PMAWBase):
    """Profile general overview."""

    @classmethod
    def from_data(cls, messari, data):
        if "overview" in data:
            data["overview"] = Overview(
                messari, _data=data["overview"]
            )

        if "roadmap" in data and isinstance(data["roadmap"], list):
            items = [item for item in data.pop("roadmap")]
            data["roadmap"] = Roadmap(messari, items)

        if "background" in data:
            data["background"] = Background(
                messari, _data=data["background"]
            )

        if "regulation" in data:
            data["regulation"] = Regulation(
                messari, _data=data["regulation"]
            )

        return cls(messari, _data=data)


class Overview(PMAWBase):
    """Profile overview."""


class Roadmap(PMAWList):
    """Profile roadmap."""


class Background(PMAWBase):
    """Profile background."""


class Regulation(PMAWBase):
    """Profile regulation."""


class Contributors(PMAWBase):
    """Profile contributors."""


class Advisors(PMAWBase):
    """Profile advisors."""


class Investors(PMAWBase):
    """Profile investors."""


class Ecosystem(PMAWBase):
    """Profile ecosystem."""

    # The asset id returned by the api here is not the same as the asset
    # id returned by the assets/asset endpoint.
    @classmethod
    def from_data(cls, messari, data):
        if "assets" in data and isinstance(data["assets"], list):
            assets = []
            for item in data["assets"]:
                assets.append(
                    asset.Asset(messari, id=item["id"])
                )
            data["assets"] = assets
        return cls(messari, _data=data)


class Economics(PMAWBase):
    """Profile economics."""


class Technology(PMAWBase):
    """Profile technology."""


class Governance(PMAWBase):
    """Profile governance."""
