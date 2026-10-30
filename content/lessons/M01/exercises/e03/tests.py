import sub


def test_round_sig():
    assert sub.round_sig(123456, 2) == 120000
    assert abs(sub.round_sig(0.0012345, 3) - 0.00123) < 1e-15
    assert abs(sub.round_sig(-98765, 1) - (-100000)) < 1e-9
    assert sub.round_sig(0, 3) == 0


def test_relative_error():
    assert abs(sub.relative_error(110, 100) - 0.1) < 1e-12
    assert abs(sub.relative_error(90, 100) - 0.1) < 1e-12


def test_factor_off_is_symmetric():
    assert abs(sub.factor_off(200, 100) - 2) < 1e-12
    assert abs(sub.factor_off(50, 100) - 2) < 1e-12
    assert sub.factor_off(7, 7) == 1


def test_factor_off_rejects_nonpositive():
    for args in [(0, 1), (1, -2)]:
        try:
            sub.factor_off(*args)
        except ValueError:
            continue
        raise AssertionError(f"factor_off{args} should raise ValueError")
