import math
import sub


def test_weights():
    assert sub.weight_bytes(7e9) == 14e9
    assert sub.weight_bytes(1e9, 4) == 4e9
    assert math.isclose(sub.to_gib(sub.weight_bytes(7e9)), 13.0385160446167, rel_tol=1e-12)


def test_adam():
    assert sub.adam_bytes(1e9) == 16e9
    # Training a 7B model needs about 104 GiB before activations: more than one 80 GiB GPU.
    assert 104 < sub.to_gib(sub.adam_bytes(7e9)) < 105


def test_max_params():
    assert sub.max_params(80, 16) == 5368709120
    assert sub.max_params(80, 2) == 42949672960
    n = sub.max_params(24, 16)
    assert n * 16 <= 24 * 2 ** 30 < (n + 1) * 16
