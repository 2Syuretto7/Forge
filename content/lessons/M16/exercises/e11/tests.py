import math
import sub


def test_guess_is_close():
    for a in (0.3, 1.0, 2.0, 7.5, 1e100, 3e-200):
        assert abs(sub.first_guess(a) / math.sqrt(a) - 1) < 0.03


def test_few_steps():
    worst = max(sub.iterations_to_full_precision(10.0 ** k, sub.first_guess(10.0 ** k)) for k in range(-300, 301, 7))
    assert worst <= 4, worst
    assert sub.iterations_to_full_precision(1e300, 1e300) > 500
