import sub


def test_published_models():
    assert sub.kv_bytes_per_token(32, 32, 128) == 524288
    assert sub.kv_bytes_per_token(32, 8, 128) == 131072
    assert sub.kv_bytes_per_token(80, 8, 128) == 327680


def test_max_batch():
    cap = 80 * 2 ** 30
    b = sub.max_batch(cap, 13.5e9, 32, 32, 128, 4096)
    assert b == int((cap - 13.5e9) // (524288 * 4096))
    assert sub.max_batch(cap, 13.5e9, 32, 8, 128, 4096) >= 4 * b
    assert sub.max_batch(cap, 140e9, 80, 8, 128, 4096) == 0
