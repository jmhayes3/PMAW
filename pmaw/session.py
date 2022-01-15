from copy import deepcopy
from urllib.parse import urljoin

from requests import codes

from .exceptions import (
    ResponseException,
    BadRequest,
    Unauthorized,
    Forbidden,
    NotFound,
    TooManyRequests,
)
from .const import API_PREFIX
from .rate_limiter import RateLimiter
from .request_handler import RequestHandler


class Session:
    # bad_gateway, gateway_timeout, internal_server_error, service_unavailable
    RETRY_CODES = {500, 502, 503, 504}

    def __init__(self, request_handler=None, api_prefix=None):
        self.request_handler = request_handler or RequestHandler()
        self.api_prefix = api_prefix or API_PREFIX

        self.rate_limiter = RateLimiter()

    def _close(self):
        self.request_handler.close()

    def __enter__(self):
        return self

    def __exit_(self, *_args):
        self._close()

    def _request_with_retries(self, method, url, params, retries=3):
        response = self.rate_limiter.call(self.request_handler.request, method, url, params)

        print(method, url, params)

        if response.status_code in self.RETRY_CODES:
            if retries > 0:
                self._request_with_retries(method, url, params, retries=retries-1)
        elif response.status_code == codes.ok:
            return response
        elif response.status_code == codes.bad_request:
            raise BadRequest(response)
        elif response.status_code == codes.unauthorized:
            raise Unauthorized(response)
        elif response.status_code == codes.forbidden:
            raise Forbidden(response)
        elif response.status_code == codes.not_found:
            raise NotFound(response)
        elif response.status_code == codes.too_many_requests:
            raise TooManyRequests(response)
        else:
            raise ResponseException(response)

    def request(self, method, path, params=None):
        params = deepcopy(params) or {}
        url = urljoin(self.api_prefix, path)

        return self._request_with_retries(method, url, params)
