# Python Messari API Wrapper (PMAW)

## Features
* Automatic rate limiting of requests.
* Pagination support for resource listings and time series data.
* Lazy loading of asset data.

## Installation
```sh
pip install --upgrade requests  # PMAW requires the requests package. 
```

```sh
pip install git+https://github.com/jmhayes3/pmaw.git@main
```

## Usage
To get started, get an instance of the Messari class:
```python
from pmaw import Messari

messari = Messari()
```

### Assets

List of top assets by market cap:
```python
for asset in messari.assets.top():
  print(asset.name)
```

### Markets

Return listing of available markets:
```python
mkts = messari.markets(limit=10)
```

Iterate over listing:
```python
for m in mkts:
  print(m.exchange_name)
 ```
 
#### Time Series
 ```python
 mt = market.timeseries("price", "2020-01-01", "2021-12-31", limit=10)
 ```
 
### News

Get news for all assets:
```python
news = messari.news(limit=10)
```
Iterate over news listing:
```python
for n in news:
  print(n.title)
```
 
