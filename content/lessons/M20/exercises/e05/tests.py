import math
import sub


def ncdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def test_grad_cdf_derivatives():
    h = 1e-6
    cases = [
        (sub.density_of_square, lambda y: math.sqrt(y), [0.1, 0.5, 0.9]),
        (sub.density_of_neglog, lambda y: 1 - math.exp(-y), [0.2, 1.0, 3.0]),
        (sub.lognormal_density, lambda y: ncdf(math.log(y)), [0.3, 1.0, 4.0]),
    ]
    for dens, cdf, ys in cases:
        for y in ys:
            assert abs((cdf(y + h) - cdf(y - h)) / (2 * h) - dens(y)) < 1e-7


def test_generic():
    d = sub.transformed_density(lambda x: 1.0, lambda y: math.exp(-y), lambda y: -math.exp(-y))
    assert abs(d(1.3) - math.exp(-1.3)) < 1e-15
    n, a, b = 20000, -12.0, 12.0
    h = (b - a) / n
    zs = [a + h * (k + 0.5) for k in range(n)]
    assert abs(sum(sub.lognormal_density(math.exp(z)) * math.exp(z) for z in zs) * h - 1) < 1e-9
