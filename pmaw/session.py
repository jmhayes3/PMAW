import logging
import traceback
import time

from datetime import datetime, timezone

from copy import deepcopy
from contextlib import contextmanager
from urllib.parse import urljoin

from requests import codes

from .exceptions import (
    ResponseException,
    TooManyRequests,
)
from .const import API_PREFIX
from .rate_limiter import RateLimiter

logger = logging.getLogger("pmaw")


class Session:
    # bad_gateway, gateway_timeout, internal_server_error, service_unavailable
    RETRY_CODES = {500, 502, 503, 504}

    def __init__(self, request_handler, api_prefix=None):
        self.request_handler = request_handler
        self.api_prefix = api_prefix or API_PREFIX

        self.rate_limiter = RateLimiter()

    def _close(self):
        self.request_handler.close()

    def __enter__(self):
        return self

    def __exit_(self, *_args):
        self._close()

    @staticmethod
    def _log_request(method, url, params):
        logger.debug(f"Request: {method} {url}; Params: {params}")

    def _request_with_retries(self, method, url, params, tries=3):
        response = self.rate_limiter.call(self.request_handler.request, method, url, params)
        self._log_request(method, url, params)

        if response.status_code == codes.ok:
            return response
        elif response.status_code in self.RETRY_CODES:
            if tries > 0:
                # use exponential backoff here
                logger.debug(f"Received {response.status_code} response. Retrying.")
                self._request_with_retries(method, url, params, tries=tries-1)
        elif response.status_code == codes.too_many_requests:
            raise TooManyRequests(response)
        else:
            raise ResponseException(response)

    def request(self, method, path, params=None):
        params = deepcopy(params) or {}
        url = urljoin(self.api_prefix, path)

        return self._request_with_retries(method, url, params)
