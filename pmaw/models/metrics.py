from .base import MessariBase, PMAWBase
from ..endpoints import API_PATH


class Metrics(MessariBase):
    """Asset metrics."""

    def __init__(self, asset, _data=None):
        super().__init__(asset._messari, _data=_data)

        self.asset = asset

    def __setattr__(self, attribute, value):
        if attribute == "market_data":
            value = MarketData.from_data(self._messari, value)
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
        path = API_PATH["asset_metrics"].format(asset=self.asset.id)
        params = {}
        return self._messari.request("GET", path, params)

    def _fetch(self):
        data = self._fetch_data().json()["data"]
        metrics = type(self)(self.asset, _data=data)

        self.__dict__.update(metrics.__dict__)

        self._fetched = True


class MarketData(PMAWBase):
    """Market data."""

    @classmethod
    def from_data(cls, messari, data):
        if "ohlcv_last_1_hour" in data:
            data["ohlcv_last_1_hour"] = OHLCV1Hour(
                messari, _data=data["ohlcv_last_1_hour"]
            )
        if "ohlcv_last_24_hour" in data:
            data["ohlcv_last_24_hour"] = OHLCV24Hour(
                messari, _data=data["ohlcv_last_24_hour"]
            )
        return cls(messari, _data=data)


class OHLCV1Hour(PMAWBase):
    """OHLCV1Hour data."""


class OHLCV24Hour(PMAWBase):
    """OHLCV24Hour data."""


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
