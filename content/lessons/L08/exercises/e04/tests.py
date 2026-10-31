import sub


def test_traffic():
    assert sub.softmax_traffic(4096, 4096, fused=False) == 201_326_592
    assert sub.softmax_traffic(4096, 4096) == 67_108_864
    assert sub.predicted_speedup(10, 30) == 3.0


def test_fits():
    assert sub.fits_on_chip(16384) and not sub.fits_on_chip(16385)
    assert sub.fits_on_chip(32768, bytes_per=2)
