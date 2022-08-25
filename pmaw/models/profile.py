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

        if "roadmap" in data:
            data["roadmap"] = Roadmap(messari, data.pop("roadmap"))

        if "background" in data:
            data["background"] = Background.from_data(messari, data.pop("background"))

        if "regulation" in data:
            data["regulation"] = Regulation(
                messari, _data=data["regulation"]
            )

        return cls(messari, _data=data)


class Overview(PMAWBase):
    """Profile overview."""


class Link(PMAWBase):
    """Link."""


class Roadmap(PMAWList):
    """Profile roadmap."""


class Background(PMAWBase):
    """Profile background."""

    @classmethod
    def from_data(cls, messari, data):
        if "issuing_organizations" in data:
            organizations = [Organization(messari, item) for item in data.pop("issuing_organizations")]
            data["issuing_organizations"] = Organizations(messari, organizations)
        return cls(messari, _data=data)


class Regulation(PMAWBase):
    """Profile regulation."""


class Contributors(PMAWBase):
    """Profile contributors."""

    @classmethod
    def from_data(cls, messari, data):
        if "individuals" in data:
            individuals = [Person(messari, item) for item in data.pop("individuals")]
            data["individuals"] = Individuals(messari, individuals)

        if "organizations" in data:
            organizations = [Organization(messari, item) for item in data.pop("organizations")]
            data["organizations"] = Organizations(messari, organizations)

        return cls(messari, _data=data)


class Advisors(PMAWBase):
    """Profile advisors."""

    @classmethod
    def from_data(cls, messari, data):
        if "individuals" in data:
            individuals = [Person(messari, item) for item in data.pop("individuals")]
            data["individuals"] = Individuals(messari, individuals)

        if "organizations" in data:
            organizations = [Organization(messari, item) for item in data.pop("organizations")]
            data["organizations"] = Organizations(messari, organizations)

        return cls(messari, _data=data)


class Investors(PMAWBase):
    """Profile investors."""

    @classmethod
    def from_data(cls, messari, data):
        if "individuals" in data:
            individuals = [Person(messari, item) for item in data.pop("individuals")]
            data["individuals"] = Individuals(messari, individuals)

        if "organizations" in data:
            organizations = [Organization(messari, item) for item in data.pop("organizations")]
            data["organizations"] = Organizations(messari, organizations)

        return cls(messari, _data=data)


class Ecosystem(PMAWBase):
    """Profile ecosystem."""

    @classmethod
    def from_data(cls, messari, data):
        if "assets" in data and isinstance(data["assets"], list):
            assets = []
            for item in data["assets"]:
                assets.append(
                    asset.Asset(messari, id=item["id"])
                )
            data["assets"] = assets

        if "organizations" in data:
            organizations = [Organization(messari, item) for item in data.pop("organizations")]
            data["organizations"] = Organizations(messari, organizations)

        return cls(messari, _data=data)


class Economics(PMAWBase):
    """Profile economics."""


class Technology(PMAWBase):
    """Profile technology."""


class Governance(PMAWBase):
    """Profile governance."""


class Person(PMAWBase):
    """Person."""


class Organization(PMAWBase):
    """Organization."""


class Individuals(PMAWList):
    """Individuals."""


class Organizations(PMAWList):
    """Organizations."""
