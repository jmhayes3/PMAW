import pytest

from pmaw.messari import Messari


@pytest.fixture
def messari():
    return Messari()


def test_messari(messari):
    assert hasattr(messari, "_session")
    assert hasattr(messari, "parser")
    assert hasattr(messari, "assets")


def test_asset(messari):
    asset = messari.asset("ethereum")
    assert hasattr(asset, "id")
    assert hasattr(asset, "_messari")
    assert hasattr(asset, "_fetched")
    assert hasattr(asset, "metrics")
    assert hasattr(asset, "profile")
    assert asset._fetched is False
    asset_slug = asset.slug
    assert asset._fetched is True
