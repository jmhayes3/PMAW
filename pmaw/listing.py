from copy import deepcopy
from urllib.parse import urljoin

from .models.base import PMAWBase
from .endpoints import API_PATH
from .exceptions import *
from .cache import cachedproperty
from .parser import Parser


class ListingGenerator(PMAWBase):

    def __init__(self, messari, path, limit=20, params=None):
        super().__init__(messari, _data=None)

        self.parser = Parser(self._messari)

        self._exhausted = False
        self._listing = None
        self._list_index = None

        self.path = path
        self.limit = limit
        self.params = params

        if self.params:
            self.params = deepcopy(params)
        else:
            self.params = {}

        self.params["limit"] = limit or 500
        self.params["page"] = 1

        self.yielded = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit is not None and self.yielded >= self.limit:
            raise StopIteration

        if self._listing is None or self._list_index >= len(self._listing):
            if self._exhausted:
                raise StopIteration

            try:
                response = self._messari.request("GET", self.path, self.params).json()
                if {"status", "data"}.issubset(response):
                    # instantiate object
                    _object = self.parser.to_object(response["data"])
                    self._listing = _object
            except NotFound:
                raise StopIteration

            if not isinstance(self._listing, list):
                raise StopIteration

            if len(self._listing) < self.params["limit"]:
                self._exhausted = True

            self._list_index = 0
            self.params["page"] += 1

        self._list_index += 1
        self.yielded += 1

        return self._listing[self._list_index - 1]


class AssetsHelper(PMAWBase):
    """Provide a set of functions to interact with a subreddit's comments."""

    def __init__(self, messari):
        super().__init__(messari, _data=None)

    def __call__(self, **generator_kwargs):
        """Return a :class:`.ListingGenerator`.

        Additional keyword arguments are passed in the initialization of
        :class:`.ListingGenerator`.

        This method should be used in a way similar to the example below:

        .. code-block:: python

            for comment in reddit.subreddit("redditdev").comments(limit=25):
                print(comment.author)

        """
        return ListingGenerator(self._messari, API_PATH["assets"], **generator_kwargs)


class AssetsListingMixin(PMAWBase):
    """Adds minimum set of methods that apply to all listing objects."""

    def __init__(self, messari, _data=None):
        super().__init__(messari, _data=_data)

    @cachedproperty
    def assets(self):
        return []
        # return AssetsHelper(self)

    def all(self, **generator_kwargs):
        generator_kwargs.setdefault("params", {})
        self._safely_add_arguments(generator_kwargs, "params", sort="id")
        path = API_PATH["assets"]
        return ListingGenerator(self._messari, path, **generator_kwargs)

    def top(self, **generator_kwargs):
        generator_kwargs.setdefault("params", {})
        path = API_PATH["assets"]
        return ListingGenerator(self._messari, path, **generator_kwargs)


class NewsListingMixin:
    """Adds additional methods pertaining to Asset-like instances."""

    def news(self):
        """Provide an instance of :class:`.NewsHelper`.

        For example, to output the author of the 25 most recent comments of
        ``r/redditdev`` execute:

        .. code-block:: python

            for comment in reddit.subreddit("redditdev").comments(limit=25):
                print(comment.author)

        """
        return None

    def __init__(self, messari, _data=None):
        """Initialize a AssetListingMixin instance.

        :param messari: An instance of :class:`.Messari`.

        """
        super().__init__(messari, _data=_data)


class TimeseriesListingMixin(PMAWBase):
    """Adds minimum set of methods that apply to all listing objects."""

    VALID_INTERVALS = {"1m", "5m", "15m", "30m", "1h", "1d", "1w"}

    @staticmethod
    def _validate_interval(interval):
        """Validate ``interval``.

        :raises: :py:class:`ValueError` if ``interval`` is not valid.

        """
        if interval not in BaseListingMixin.VALID_INTERVALS:
            valid_intervals = ", ".join(BaseListingMixin.VALID_INTERVALS)
            raise ValueError(f"interval must be one of: {valid_intervals}")

    def top(self, interval="1d", **generator_kwargs):
        self._validate_interval(interval)
        self._safely_add_arguments(generator_kwargs, "params", interval=interval)
        return ListingGenerator(self._reddit, path, **generator_kwargs)


class Listing(PMAWBase):
    """A listing is a collection of RedditBase instances."""

    CHILD_ATTRIBUTE = "children"

    def __len__(self):
        """Return the number of items in the Listing."""
        return len(getattr(self, self.CHILD_ATTRIBUTE))

    def __getitem__(self, index):
        """Return the item at position index in the list."""
        return getattr(self, self.CHILD_ATTRIBUTE)[index]

    def __setattr__(self, attribute, value):
        """Objectify the CHILD_ATTRIBUTE attribute."""
        if attribute == self.CHILD_ATTRIBUTE:
            value = self._reddit._objector.objectify(value)
        super().__setattr__(attribute, value)


class AssetListing(Listing):
    """Special Listing for handling asset lists."""

    CHILD_ATTRIBUTE = "data"


# class BaseList(PMAWBase):
#     """An abstract class to coerce a list into a PMAWBase."""

#     CHILD_ATTRIBUTE = None

#     def __init__(self, reddit: "praw.Reddit", _data: Dict[str, Any]):
#         """Initialize a BaseList instance.

#         :param reddit: An instance of :class:`~.Reddit`.

#         """
#         super().__init__(reddit, _data=_data)

#         if self.CHILD_ATTRIBUTE is None:
#             raise NotImplementedError("BaseList must be extended.")

#         child_list = getattr(self, self.CHILD_ATTRIBUTE)
#         for index, item in enumerate(child_list):
#             child_list[index] = reddit._objector.objectify(item)

#     def __contains__(self, item: Any) -> bool:
#         """Test if item exists in the list."""
#         return item in getattr(self, self.CHILD_ATTRIBUTE)

#     def __getitem__(self, index: int) -> Any:
#         """Return the item at position index in the list."""
#         return getattr(self, self.CHILD_ATTRIBUTE)[index]

#     def __iter__(self) -> Iterator[Any]:
#         """Return an iterator to the list."""
#         return getattr(self, self.CHILD_ATTRIBUTE).__iter__()

#     def __len__(self) -> int:
#         """Return the number of items in the list."""
#         return len(getattr(self, self.CHILD_ATTRIBUTE))

#     def __str__(self) -> str:
#         """Return a string representation of the list."""
#         return str(getattr(self, self.CHILD_ATTRIBUTE))
