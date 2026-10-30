import math
import sub


def test_evaluate():
    assert sub.evaluate(("/", ("sin", ("x",)), ("x",)), 0.5) == math.sin(0.5) / 0.5
    assert sub.evaluate(("tanh", ("log", ("x",))), 2.0) == math.tanh(math.log(2.0))


def test_grad_all_thirty_verified():
    assert len(sub.FUNCTIONS) == 30
    for i, (e, x) in enumerate(sub.FUNCTIONS):
        ok, err, allowed = sub.verify(e, x)
        assert ok, f"function {i}: error {err:.2e} above the budget {allowed:.2e}"
        assert allowed < 1e-6 * max(1.0, abs(sub.evaluate(sub.derivative(e), x))), f"function {i}: the budget is too loose to mean anything"


def test_grad_planted_errors_are_caught():
    X = ("x",)
    wrong = [
        (("sin", X), ("*", ("c", -1.0), ("cos", X)), 0.4),
        (("log", X), ("/", ("c", 1.0), ("^", X, 2)), 2.5),
        (("tanh", X), ("+", ("c", 1.0), ("^", ("tanh", X), 2)), 0.8),
        (("/", c := ("c", 1.0), X), ("/", c, ("^", X, 2)), 0.6),
        (("exp", ("*", ("c", -2.0), X)), ("exp", ("*", ("c", -2.0), X)), 0.3),
    ]
    for e, d, x in wrong:
        ok, err, allowed = sub.verify(e, x, d)
        assert not ok, (e, err, allowed)
