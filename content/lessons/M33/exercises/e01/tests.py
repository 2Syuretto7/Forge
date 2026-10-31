import sub


def test_puzzle_numbers():
    f = sub.matmul_flops(4096, 4096, 4096)
    assert f == 137438953472
    b = sub.matmul_bytes(4096, 4096, 4096)
    assert b == 3 * 4096 * 4096 * 4
    assert abs(sub.intensity(f, b) - 4096 / 6) < 1e-9


def test_matvec_is_starved():
    i = sub.matvec_intensity(4096, 4096)
    assert 0.49 < i < 0.5
    assert sub.intensity(sub.matmul_flops(4096, 4096, 4096), sub.matmul_bytes(4096, 4096, 4096)) > 1000 * i
    assert sub.matmul_bytes(10, 10, 10, word=8) == 2400
