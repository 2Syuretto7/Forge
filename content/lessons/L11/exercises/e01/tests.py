import sub


def test_matmul():
    assert sub.matmul_cost(64, 512, 512) == (2 * 64 * 512 * 512, 2 * (64 * 512 + 512 * 512 + 64 * 512))
    assert abs(sub.intensity(sub.matmul_cost(4096, 4096, 4096)) - 4096 / 3) < 1e-9
    assert sub.matmul_cost(2, 3, 4, bytes_per=4) == (48, 4 * (8 + 12 + 6))


def test_elementwise():
    assert sub.elementwise_cost(1_000_000, 1, 2, bytes_per=4) == (1_000_000, 12_000_000)
    f, b = sub.elementwise_cost(10, 8, 1)
    assert (f, b) == (80, 40)


def test_softmax():
    assert sub.softmax_cost(32, 1000) == (160_000, 128_000)
    assert abs(sub.intensity(sub.softmax_cost(8, 8, bytes_per=4)) - 5 / 8) < 1e-12
