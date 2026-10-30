import math
import sub


def test_cases():
    assert sub.solve_linear(3, 2, 11) == 3
    assert math.isclose(sub.solve_linear(-4, 1, 0), 0.25)
    assert sub.solve_linear(0, 2, 2) == "all"
    assert sub.solve_linear(0, 2, 5) is None


def test_solution_satisfies_the_equation():
    for a, b, c in [(2.5, -1, 7), (-0.1, 3, 3.3), (7, 7, 7)]:
        x = sub.solve_linear(a, b, c)
        assert abs(a * x + b - c) < 1e-12


def test_utilization():
    u = sub.utilization(8.333333333333334, 1e8, 2e9, 1e14)
    assert math.isclose(u, 0.4, rel_tol=1e-12)
    hours = 6 * 1e8 * 2e9 / (1e14 * u * 3600)
    assert math.isclose(hours, 8.333333333333334, rel_tol=1e-12)
