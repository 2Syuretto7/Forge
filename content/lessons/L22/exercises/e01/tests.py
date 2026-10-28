import sub


def test_intensities():
    assert sub.decode_intensity(7e9, 1, 0) == 1.0
    assert sub.decode_intensity(7e9, 32, 0) == 32.0
    assert sub.decode_intensity(7e9, 32, 14e9) == 16.0
    assert sub.prefill_intensity(7e9, 1000) == 1000.0


def test_step_time():
    t = sub.step_time(2 * 7e9, 14e9, 65e12, 320e9)
    assert abs(t - 14e9 / 320e9) < 1e-15
    assert sub.step_time(2e15, 1e9, 65e12, 320e9) == 2e15 / 65e12
