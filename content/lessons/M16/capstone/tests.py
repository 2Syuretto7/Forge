import sub

REP = sub.report()


def test_problems_are_minima():
    for name, f, df, d2f, x0, xs in sub.PROBLEMS:
        assert abs(df(xs)) < 1e-12 and d2f(xs) > 0, name


def test_grad_gradient_descent_linear():
    for r in REP:
        assert abs(r["gd_order"] - 1) < 0.1, r
        assert abs(r["gd_rate"] - r["gd_predicted_rate"]) < 0.1 * r["gd_predicted_rate"], r


def test_grad_secant_superlinear():
    for r in REP:
        assert abs(r["secant_order"] - 1.618) < 0.1 * 1.618, r


def test_grad_newton_quadratic():
    for r in REP:
        assert abs(r["newton_order"] - 2) < 0.2, r
