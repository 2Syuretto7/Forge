import sub


def test_bytes():
    assert sub.bytes_per_param("adam", True) == 16 and sub.bytes_per_param("adam", False) == 16
    assert sub.bytes_per_param("sgd", True) == 8 and sub.bytes_per_param("sgd", False) == 8


def test_gb():
    assert abs(sub.training_memory_gb(7e9) - 112) < 1e-9
    assert abs(sub.inference_memory_gb(7e9) - 14) < 1e-9
    assert abs(sub.inference_memory_gb(7e9, 1) - 7) < 1e-9
