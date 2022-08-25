from .base import PMAWBase, PMAWList
from ..endpoints import API_PATH
from ..listing import ListingGenerator


class News(PMAWBase):
    """News item."""

    @classmethod
    def from_data(cls, messari, data):
        if "references" in data:
            references = [Reference(messari, item) for item in data.pop("references")]
            data["references"] = References(messari, references)

        if "author" in data:
            author = Author(messari, _data=data.pop("author"))
            data["author"] = author

        return cls(messari, _data=data)


class Reference(PMAWBase):
    """Reference."""


class References(PMAWList):
    """Reference list."""


class Author(PMAWBase):
    """Author data."""
