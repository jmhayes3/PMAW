from .base import MessariBase, PMAWBase
from ..endpoints import API_PATH
from ..util import flatten


class Metrics(MessariBase):
    """Asset metrics."""

    def __init__(self, messari, id=None, _data=None, _fetched=False):
        if (id, _data).count(None) != 1:
            raise TypeError("Either `id` or `_data` required.")

        if id:
            self.id = id

        super().__init__(messari, _data=_data, _fetched=_fetched, _str_field=False)

    def __setattr__(self, attribute, value):
        if attribute == "market_data":
            value = MarketData.from_data(self._messari, flatten(value))
            # value = self._messari.parser.parse(value)
        elif attribute == "supply":
            value = Supply.from_data(self._messari, value)
        elif attribute == "blockchain_stats_24_hours":
            value = BlockchainStats24Hours.from_data(self._messari, value)
        elif attribute == "all_time_high":
            value = AllTimeHigh.from_data(self._messari, value)
        elif attribute == "developer_activity":
            value = DeveloperActivity.from_data(self._messari, value)
        elif attribute == "roi_data":
            value = ROIData.from_data(self._messari, value)
        elif attribute == "misc_data":
            value = MiscData.from_data(self._messari, value)

        super().__setattr__(attribute, value)

    def _fetch_data(self):
        path = API_PATH["asset_metrics"].format(asset=self.id)
        params = {}
        return self._messari.request("GET", path, params)

    def _fetch(self):
        data = self._fetch_data()
        metrics_data = data.json()["data"]
        metrics = type(self)(self._messari, _data=metrics_data)

        self.__dict__.update(metrics.__dict__)

        self._fetched = True


class MarketData(PMAWBase):
    """Market data."""


class Supply(PMAWBase):
    """Supply data."""


class BlockchainStats24Hours(PMAWBase):
    """Blockchain 24 hour stats."""


class AllTimeHigh(PMAWBase):
    """All time high data."""


class DeveloperActivity(PMAWBase):
    """Developer activity data."""


class ROIData(PMAWBase):
    """ROI data."""


class MiscData(PMAWBase):
    """Misc data."""
