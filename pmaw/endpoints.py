"""List of known API endpoints."""

API_PATH = {
    "assets":                       "api/v2/assets",
    "markets":                      "api/v1/markets",
    "news":                         "api/v1/news",
    "asset":                        "api/v1/assets/{asset}",
    "asset_profile":                "api/v2/assets/{asset}/profile",
    "asset_metrics":                "api/v1/assets/{asset}/metrics",
    "asset_market_data":            "api/v1/assets/{asset}/metrics/market-data",
    "asset_metric_time_series":     "api/v1/assets/{asset}/metrics/{metric}/time-series",
    "asset_news":                   "api/v1/news/{asset}",
    "assets_supported_metrics":     "api/v1/assets/metrics",
    "market_metric_time_series":    "api/v1/markets/{market}/metrics/{metric}/time-series",
}
