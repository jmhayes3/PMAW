"""List of known API endpoints."""

API_PATH = {
    "assets":                       "api/v2/assets",
    "markets":                      "api/v1/markets",
    "news":                         "api/v1/news",
    "asset":                        "api/v1/assets/{asset_key}",
    "asset_profile":                "api/v2/assets/{asset_key}/profile",
    "asset_metrics":                "api/v1/assets/{asset_key}/metrics",
    "asset_market_data":            "api/v1/assets/{asset_key}/metrics/market-data",
    "assset_metrics_list":          "api/v1/assets/metrics",
    "assset_metric_time_series":    "api/v1/assets/{asset_key}/metrics/{metric_id}/time-series",
    "asset_news":                   "api/v1/news/{asset_key}",
    "market_metric_time_series":    "api/v1/markets/{market_key}/metrics/{metric_id}/time-series",
}
