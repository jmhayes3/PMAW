# Python Messari API Wrapper (PMAW)

[![build](https://github.com/jmhayes3/pmaw/actions/workflows/ci.yml/badge.svg)](https://github.com/jmhayes3/pmaw/actions/workflows/ci.yml)

PMAW is a Python package that allows for simple access to the [Messari](https://messari.io) API.
PMAW aims to be robust and easy to use while respecting [Messari's API rules](https://messari.io/api/docs).

## Installation
```sh
pip install git+https://github.com/jmhayes3/pmaw.git
```

## Usage
To get started, create an instance of the ``Messari`` class:
```python
from pmaw import Messari

messari = Messari()
```

To authenticate using an API key, pass the key in like so:
```python
messari = Messari(api_key="<your-api-key>")
```

Or, set the ``X_MESSARI_API_KEY`` environmental variable:
```sh
export X_MESSARI_API_KEY=<your-api-key>
```

Using the ``messari`` instance you can then interact with the API:
```python
# Get the top 10 assets by market cap.
for asset in messari.assets.top(limit=10):
  print(asset.name)

# Markets
for market in messari.markets(limit=5):
  print(market.exchange_name, market.pair)

# Time Series

# News
news = messari.news(limit=10)
for n in news:
  print(n.title)
```

To check which attributes are available for an object use the ``vars`` function:
```python
asset = messari.asset("eth")
vars(asset)
```

## Rate Limits
PMAW handles rate limiting automatically, eliminating the need to introduce sleep calls into code.

By default, the rate limit is set to 20 requests per minute (the limit enforced by the API for unauthenticated users).
If an API key is provided, the rate limit is increased to 30 requests per minute.
A custom rate limit can be set using the ``target_rate`` keyword argument when initializing the ``Messari`` class. 
