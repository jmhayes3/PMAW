from .base import MessariBase
from ..endpoints import API_PATH

from ..listing import AssetsListingMixin


class Assets(AssetsListingMixin):

    PATH = "api/v2/assets"
    PARAMS = {"fields": "id,slug,symbol,name"}

    def __init__(self, messari, _data=None):
        super().__init__(messari, _data=_data)

    def __setattr__(self, attribute, value):
        super().__setattr__(attribute, value)

    def supported_metrics(self):
        path = API_PATH["assets_supported_metrics"]
        return self._messari.request("GET", path)
