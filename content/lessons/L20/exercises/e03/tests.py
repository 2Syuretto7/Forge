import sub


def test_schedule():
    assert abs(sub.lr_at(50, 1e-3, 100, 1000) - 5e-4) < 1e-15
    assert abs(sub.lr_at(100, 1e-3, 100, 1000) - 1e-3) < 1e-15
    assert abs(sub.lr_at(550, 1e-3, 100, 1000) - 5.5e-4) < 1e-15
    assert abs(sub.lr_at(1000, 1e-3, 100, 1000) - 1e-4) < 1e-15
    assert sub.lr_at(700, 1e-3, 100, 1000) < sub.lr_at(600, 1e-3, 100, 1000)


def test_steps():
    assert sub.steps_for_tokens(1e6, 32, 256) == 123
    assert sub.steps_for_tokens(8192, 32, 256) == 1
