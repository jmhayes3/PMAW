from .base import MessariBase, PMAWBase
from ..endpoints import API_PATH

from . import asset


class Profile(MessariBase):
    """Asset profile."""

    def __init__(self, messari, id=None, _data=None, _fetched=False):
        if (id, _data).count(None) != 1:
            raise TypeError("Either `id` or `_data` required.")

        if id:
            self.id = id
        elif _data:
            _fetched = True

        super().__init__(messari, _data=_data, _fetched=_fetched)

    def __setattr__(self, attribute, value):
        if attribute == "general":
            value = self._messari.parser.parse(value)
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

    def _fetch_data(self):
        path = API_PATH["asset_profile"].format(asset=self.id)
        params = {}
        # params = {
        #     "as-markdown": "",
        # }
        return self._messari.request("GET", path, params)

    def _fetch(self):
        data = self._fetch_data()
        profile_data = data.json()["data"]
        profile = type(self)(self._messari, _data=profile_data)

        for attribute, value in profile.profile.items():
            setattr(self, attribute, value)

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
            roadmap = data.pop("roadmap")
            roadmap_list = [RoadmapItem(messari, item) for item in roadmap]
            data["roadmap"] = Roadmap(messari, roadmap_list)

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


class Roadmap(PMAWBase):
    """Profile roadmap."""

    def __init__(self, messari, items, _data=None):
        super().__init__(messari, _data=_data)

        self.items = items or []

    def __getitem__(self, index):
        return self.items[index]

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)


class RoadmapItem(PMAWBase):
    """Roadmap item."""


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

    @classmethod
    def from_data(cls, messari, data):
        if "assets" in data and isinstance(data["assets"], list):
            assets = []
            for item in data["assets"]:
                assets.append(
                    asset.Asset(messari, id=item.get("name"))
                )
            data["assets"] = assets
        return cls(messari, _data=data)


class Economics(PMAWBase):
    """Profile economics."""


class Technology(PMAWBase):
    """Profile technology."""


class Governance(PMAWBase):
    """Profile governance."""
