import sub


def test_kv():
    assert sub.kv_bytes(32, 32, 128, 4096) == 2 ** 31
    assert sub.max_sequences(80e9, 13.48e9, 32, 32, 128, 4096) == 27
    assert sub.max_sequences(16e9, 15e9, 32, 32, 128, 4096) == 0
    assert abs(sub.decode_step_ms(13.48e9, 0, 2.04e12) - 6.608) < 0.001
