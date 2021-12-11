from .base import MessariBase
from ..endpoints import API_PATH

from ..listing import AssetListingMixin


class Assets(AssetListingMixin):

    def __init__(self, messari, _data=None):
        super().__init__(messari, _data=_data)

    def __setattr__(self, attribute, value):
        super().__setattr__(attribute, value)

    @property
    def supported_metrics(self):
        path = API_PATH["assets_supported_metrics"]
        return self._messari.request("GET", path).json()["data"]["metrics"]
