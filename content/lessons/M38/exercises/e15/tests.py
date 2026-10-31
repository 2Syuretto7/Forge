import sub


def test_adam_fails_amsgrad_works():
    assert sub.run(False) == 1.0
    assert abs(sub.run(True) + 1) < 0.01
    assert sub.average_loss_slope() > 0
