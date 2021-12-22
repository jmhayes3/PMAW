class PMAWException(Exception):
    """Base exception class."""


class RequestException(PMAWException):
    """An exception occurred while handling the request."""

    def __init__(self, original_exception, request_args, request_kwargs):
        self.original_exception = original_exception
        self.request_args = request_args
        self.request_kwargs = request_kwargs

        super(RequestException, self).__init__(
            f"error with request {original_exception}"
        )


class ResponseException(PMAWException):
    """An exception occurred after the request was completed."""

    def __init__(self, response):
        self.response = response

        super(ResponseException, self).__init__(
            f"{response.status_code} response received."
        )


class BadRequest(ResponseException):
    """Indicate invalid parameters for the request."""


class Unauthorized(ResponseException):
    """Indicate a conflicting change in the target resource."""


class Forbidden(ResponseException):
    """Indicate the authentication is not permitted for the request."""


class NotFound(ResponseException):
    """Indicate that the requested URL was not found."""


class TooManyRequests(ResponseException):
    """Too many requests made."""

    def __init__(self, response):
        self.response = response
        self.retry_after = response.headers.get("retry-after")

        msg = "Too many requests."
        if self.retry_after:
            _wait = float(self.retry_after)
            msg += f" Wait {_wait} seconds before retrying this request."
        PMAWException.__init__(self, msg)
