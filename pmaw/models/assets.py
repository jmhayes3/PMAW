from .base import PMAWBase
from ..endpoints import API_PATH
from ..listing import ListingGenerator


class Assets(PMAWBase):
    """Assets."""

    def __init__(self, messari, _data=None):
        super().__init__(messari, _data=_data)

    def all(self, with_metrics=False, with_profiles=False, **generator_kwargs):
        generator_kwargs.setdefault("params", {})

        self._safely_add_arguments(generator_kwargs, "params", sort="id")

        if with_metrics:
            self._safely_add_argument(
                generator_kwargs,
                "params",
                "with-metrics",
                ""
            )

        if with_profiles:
            self._safely_add_argument(
                generator_kwargs,
                "params",
                "with-profiles",
                ""
            )

        return ListingGenerator(
            self._messari,
            API_PATH["assets"],
            **generator_kwargs
        )

    def top(self, with_metrics=False, with_profiles=False, **generator_kwargs):
        generator_kwargs.setdefault("params", {})

        if with_metrics:
            self._safely_add_argument(
                generator_kwargs,
                "params",
                "with-metrics",
                ""
            )

        if with_profiles:
            self._safely_add_argument(
                generator_kwargs,
                "params",
                "with-profiles",
                ""
            )

        return ListingGenerator(
            self._messari,
            API_PATH["assets"],
            **generator_kwargs
        )

    @property
    def supported_metrics(self):
        return self._messari.request(
            "GET",
            API_PATH["assets_supported_metrics"]
        ).json()["data"]["metrics"]
