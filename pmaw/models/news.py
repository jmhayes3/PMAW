from .base import PMAWBase


class News(PMAWBase):
    """News."""


class NewsItem(PMAWBase):
    """News item."""

    @classmethod
    def from_data(cls, messari, data):
        if "references" in data:
            references = []
            for item in data.pop("references"):
                references.append(
                    Reference(messari, _data=item)
                )
            data["references"] = references

        if "author" in data:
            author = Author(messari, _data=data.pop("author"))
            data["author"] = author

        return cls(messari, _data=data)


class Reference(PMAWBase):
    """Reference data."""


class Author(PMAWBase):
    """Author data."""
