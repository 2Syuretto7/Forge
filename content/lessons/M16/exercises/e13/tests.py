import math
import sub

f = lambda x: x ** 3 - 2 * x + 2  # noqa: E731
df = lambda x: 3 * x * x - 2  # noqa: E731


def test_cycle():
    orbit = sub.newton_orbit(f, df, 0.0, 20)
    assert orbit[:3] == [0.0, 1.0, 0.0]
    assert sub.cycle_length(orbit) == 2


def test_cube_root_diverges():
    g = lambda x: math.copysign(abs(x) ** (1 / 3), x)  # noqa: E731
    dg = lambda x: abs(x) ** (-2 / 3) / 3  # noqa: E731
    orbit = sub.newton_orbit(g, dg, 0.1, 10)
    assert abs(orbit[10]) > 50 and abs(orbit[1] + 0.2) < 1e-12
    assert sub.cycle_length(orbit) is None


def test_damped():
    r = sub.damped_newton(f, df, 0.0)
    assert abs(f(r)) < 1e-12 and abs(r + 1.7692923542386314) < 1e-10
