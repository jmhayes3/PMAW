"""PMAW: Python Messari API Wrapper."""

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

_stream_handler = logging.StreamHandler()
_stream_handler.setLevel(logging.INFO)

log.addHandler(_stream_handler)
