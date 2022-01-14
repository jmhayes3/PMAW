from .base import PMAWBase
from ..endpoints import API_PATH
from ..listing import ListingGenerator


class Assets(PMAWBase):
    """Assets.

    page    integer Page number, starts at 1. Increment to paginate through
            results (until result is empty array)
    sort    string default sort is "marketcap desc", but the only valid value
            for this query param is "id" which translates to "id asc", which is
            useful for a stable sort while paginating
    limit    integer default is 20, max is 500
    fields    string pare down the returned fields (comma , separated, drill down with a slash /)
    with-metrics    any existence of this query param filters assets to those with quantitative data
    with-profiles    any existence of this query param filters assets to those with qualitative data
    """

    def __init__(self, messari, _data=None):
        super().__init__(messari, _data=_data)

    def all(self, **generator_kwargs):
        generator_kwargs.setdefault("params", {})
        self._safely_add_arguments(generator_kwargs, "params", sort="id")
        path = API_PATH["assets"]
        return ListingGenerator(self._messari, path, **generator_kwargs)

    def top(self, **generator_kwargs):
        generator_kwargs.setdefault("params", {})
        path = API_PATH["assets"]
        return ListingGenerator(self._messari, path, **generator_kwargs)

    @property
    def supported_metrics(self):
        path = API_PATH["assets_supported_metrics"]
        return self._messari.request("GET", path).json()["data"]["metrics"]
