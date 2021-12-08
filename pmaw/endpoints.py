"""List of known API endpoints."""

API_PATH = {
    "assets":                       "api/v2/assets",
    "markets":                      "api/v1/markets",
    "news":                         "api/v1/news",
    "asset":                        "api/v1/assets/{asset}",
    "asset_profile":                "api/v2/assets/{asset}/profile",
    "asset_metrics":                "api/v1/assets/{asset}/metrics",
    "asset_market_data":            "api/v1/assets/{asset}/metrics/market-data",
    "asset_metrics_list":           "api/v1/assets/metrics",
    "asset_metric_time_series":     "api/v1/assets/{asset}/metrics/{metric_id}/time-series",
    "asset_news":                   "api/v1/news/{asset}",
    "market_metric_time_series":    "api/v1/markets/{market}/metrics/{metric_id}/time-series",
}
