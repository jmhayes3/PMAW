from pmaw.messari import Messari


def test_pmaw():
    messari = Messari()
    assert hasattr(messari, "_session")
    assert hasattr(messari, "parser")
    assert hasattr(messari, "assets")
    assert messari._max_wait == 60
