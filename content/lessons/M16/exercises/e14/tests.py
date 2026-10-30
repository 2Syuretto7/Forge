import sub


def test_quadratic():
    xs = sub.gd_quadratic(4.0, 0.6, 1.0, 10)
    assert abs(abs(xs[10]) - 1.4 ** 10) < 1e-9
    assert sub.growth(4.0, 0.6) > 1 > sub.growth(4.0, 0.4)
    assert sub.first_blowup(None, lambda x: 4 * x, 1.0, 0.6) == 42


def test_quartic():
    df = lambda x: 2 * x + x ** 3  # noqa: E731
    etas = [0.1, 0.2, 0.5, 0.8, 0.95, 0.99, 1.01, 1.1]
    assert sub.largest_safe_eta(df, 0.01, etas, steps=2000) == 0.99
    assert sub.largest_safe_eta(df, 1.5, etas) <= 0.2, "far from 0 the curvature is larger, so the safe step is smaller"
