from copy import deepcopy
from urllib.parse import urljoin

from .models.base import PMAWBase
from .endpoints import API_PATH
from .exceptions import NotFound


class ListingGenerator(PMAWBase):

    def __init__(self, messari, path, limit=500, params=None):
        super().__init__(messari, _data=None)

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
                    data = response.get("data")
                    self._listing = self._messari.parser.parse(data)
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


class TimeseriesGenerator(PMAWBase):
    """
    Get Asset timeseries

    Retrieve historical timeseries data for an asset.
    metricID specifies which timeseries will be returned. The list of supported metric ids can be found at https://data.messari.io/api/v1/assets/metrics.

    You can specify the range of what points will be returned using (begin, end, start, before, after) query parameters. All range parameters are inclusive of the specified date.

    Some examples:

    Return data between 2019-01-01 to 2019-01-07: "?start=2020-01-01&end=2020-01-07"
    Return data after 2020-01-01: "?after=2020-01-01"
    Return data before 2020-01-01: "?before=2020"

    You can specify the interval that the points will be returned in using the "interval" query parameter. Supported intervals are ["5m", "15m", "30m", "1h", "1d", "1w"] for 5 minute, 15 minute, 30 minute. 1 hour, 1 day, and 1 week respectively. Anything under 1 day requires an enterprise subscription, please email enterprise@messari.io.

    A default start date, end date, and/or interval will be provided for you if not specified.

    For any given interval, at most 2016 points will be returned. For example, with interval=5m, the maximum range of the request is 2016 * 5 minutes = 7 days. With interval=1h, the maximum range is 2016 * 1 hour = 84 days. Exceeding the maximum range will result in an error, which can be solved by reducing the date range specified in the request.

    You can specify the sort order of data points in the response using the ?order query parameter. Supported values are "asc" and "desc".

    You can specify the format of the response using the "format" query parameter. Supported formats are "json" and "csv"
    """

    def __init__(self, messari, path, limit=500, params=None):
        super().__init__(messari, _data=None)

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
                    data = response.get("data")
                    self._listing = self._messari.parser.parse(data)
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
