# Python Messari API Wrapper (PMAW)

## Features
* Automatic rate limiting of requests.
* Pagination support for resource listings and time series data.
* Lazy loading of asset data.

## Installation

```sh
pip install requests

pip install git+https://github.com/jmhayes3/pmaw.git@main
```

## Usage

```python
from pmaw import Messari

messari = Messari()
```

Return list of top assets by market cap:
```python
for asset in messari.assets.top():
  print(asset.name)
```
