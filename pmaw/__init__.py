"""PMAW: Python Messari API Wrapper."""

import logging

from .messari import Messari

logging.getLogger(__name__).addHandler(logging.NullHandler())
