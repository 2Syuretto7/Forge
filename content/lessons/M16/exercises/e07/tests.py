import math
import sub


def test_quadratic():
    L = 4.0
    for eta in (0.1, 0.4, 0.45, 0.55):
        xs = sub.gd(lambda x: L * x, 1.0, eta, 20)
        assert abs(abs(xs[20]) - sub.predicted_factor(eta, L) ** 20) < 1e-12
    assert sub.step_limit(L) == 0.5


def test_grad_descent_lemma():
    f = lambda x: math.log(math.cosh(x))  # noqa: E731
    df = math.tanh
    for x in (-3.0, -0.5, 0.2, 1.0, 4.0):
        for eta in (0.1, 0.5, 1.0, 1.5, 1.9):
            actual, guaranteed = sub.descent_bound(f, df, x, eta, 1.0)
            assert actual >= guaranteed - 1e-12, (x, eta)
            assert guaranteed > 0
