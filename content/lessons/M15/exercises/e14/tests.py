import sub


def test_jump():
    assert sub.jump_central(1e-3) == 500.0
    assert abs(sub.blowup_rate([1e-1, 1e-2, 1e-3, 1e-4]) + 1) < 1e-9


def test_grad_smoothed_slope():
    for w in (1.0, 0.1, 0.01):
        h = 1e-4 * w
        slope = (sub.smoothed_step(h, w) - sub.smoothed_step(-h, w)) / (2 * h)
        assert abs(slope - 1 / (4 * w)) < 1e-6 / w
