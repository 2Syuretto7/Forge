import math
import sys

import sub

XS = [10.0 ** k for k in range(-3, 9)]


def test_steps():
    assert abs(sub.scaled_step(1e8, "forward") - 1.49e-8 * 1e8) < 1e-2
    assert abs(sub.scaled_step(0.5, "central") - 3.03e-6) < 1e-8
    assert sub.scaled_step(0.0, "central") == sys.float_info.epsilon ** (1 / 3)


def test_grad_log_passes_everywhere():
    assert sub.check_derivative(math.log, lambda x: 1 / x, XS) == []


def test_fixed_step_would_fail():
    h = 1e-5
    bad = [x for x in XS if abs((math.log(x + h) - math.log(x - h)) / (2 * h) - 1 / x) * x > 1e-6]
    assert bad, "a fixed step fails somewhere in this range"


def test_catches_typo():
    bad = sub.check_derivative(lambda x: math.sin(x) * x, lambda x: math.cos(x) * x - math.sin(x), [0.5, 1.0, 2.0])
    assert len(bad) == 3
