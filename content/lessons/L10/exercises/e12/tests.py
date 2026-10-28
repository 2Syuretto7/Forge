import numpy as np
import sub

RESULT = sub.warmup_experiment()


def test_dead_fraction_detects_dead_units():
    X, _ = sub.make_digits(50, 1)
    p = sub.init_stack(3, 8)
    assert sub.dead_fraction(p, X, 3, "post") == [0.0, 0.0, 0.0]
    # In the plain stack, layer 1 sees ReLU outputs, which are never negative, so a column of
    # W1 with only negative entries can never fire.
    p["W1"][:, :2] = -1.0
    d = sub.dead_fraction(p, X, 3, "plain")
    assert len(d) == 3 and d[1] >= 0.25


def test_warmup_rescues_post_norm():
    none, warm = RESULT["none"], RESULT["warmup"]
    assert none[0] > 1.8, RESULT
    assert warm[0] < none[0] - 0.3, RESULT


def test_more_dead_units_without_warmup():
    assert RESULT["none"][1] > RESULT["warmup"][1], RESULT
