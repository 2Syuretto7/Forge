import math

# provided
INTEGRALS = [
    {"name": "x^2 on [0, 1]", "f": lambda x: x * x, "a": 0.0, "b": 1.0, "singular": False, "exact": 1 / 3},
    {"name": "sin on [0, pi]", "f": math.sin, "a": 0.0, "b": math.pi, "singular": False, "exact": 2.0},
    {"name": "exp on [0, 1]", "f": math.exp, "a": 0.0, "b": 1.0, "singular": False, "exact": math.e - 1},
    {"name": "1/x on [1, 2]", "f": lambda x: 1 / x, "a": 1.0, "b": 2.0, "singular": False, "exact": math.log(2)},
    {"name": "1/(1+x^2) on [0, 1]", "f": lambda x: 1 / (1 + x * x), "a": 0.0, "b": 1.0, "singular": False, "exact": math.pi / 4},
    {"name": "sqrt(x) on [0, 1]", "f": math.sqrt, "a": 0.0, "b": 1.0, "singular": True, "exact": 2 / 3},
    {"name": "1/sqrt(x) on [0, 1]", "f": lambda x: x ** -0.5, "a": 0.0, "b": 1.0, "singular": True, "exact": 2.0},
    {"name": "log(x) on [0, 1]", "f": math.log, "a": 0.0, "b": 1.0, "singular": True, "exact": -1.0},
    {"name": "exp(-x) on [0, inf)", "f": lambda x: math.exp(-x), "a": 0.0, "b": math.inf, "singular": False, "exact": 1.0},
    {"name": "Gaussian on the line", "f": lambda x: math.exp(-x * x / 2), "a": -math.inf, "b": math.inf, "singular": False, "exact": math.sqrt(2 * math.pi)},
    {"name": "1/(1+x^2) on [0, inf)", "f": lambda x: 1 / (1 + x * x), "a": 0.0, "b": math.inf, "singular": False, "exact": math.pi / 2},
    {"name": "Beta(2.5, 3.5) normalizer", "f": lambda x: x ** 1.5 * (1 - x) ** 2.5, "a": 0.0, "b": 1.0, "singular": False, "exact": math.gamma(2.5) * math.gamma(3.5) / math.gamma(6.0)},
    {"name": "sin(20x) on [0, 1]", "f": lambda x: math.sin(20 * x), "a": 0.0, "b": 1.0, "singular": False, "exact": (1 - math.cos(20)) / 20},
    {"name": "|x - 1| on [0, 2]", "f": lambda x: abs(x - 1), "a": 0.0, "b": 2.0, "singular": False, "exact": 1.0},
    {"name": "narrow peak", "f": lambda x: math.exp(-100 * (x - 0.5) ** 2), "a": 0.0, "b": 1.0, "singular": False, "exact": math.sqrt(math.pi / 100) * math.erf(5)},
    {"name": "exp(-x)/sqrt(x) on [0, 1]", "f": lambda x: math.exp(-x) / math.sqrt(x), "a": 0.0, "b": 1.0, "singular": True, "exact": math.sqrt(math.pi) * math.erf(1)},
    {"name": "x exp(-x^2) on [0, inf)", "f": lambda x: x * math.exp(-x * x), "a": 0.0, "b": math.inf, "singular": False, "exact": 0.5},
    {"name": "cos^2 on [0, 1]", "f": lambda x: math.cos(x) ** 2, "a": 0.0, "b": 1.0, "singular": False, "exact": 0.5 + math.sin(2) / 4},
    {"name": "1/(x + 0.01) on [0, 1]", "f": lambda x: 1 / (x + 0.01), "a": 0.0, "b": 1.0, "singular": False, "exact": math.log(101)},
    {"name": "log(sin x) on [0, pi/2]", "f": lambda x: math.log(math.sin(x)), "a": 0.0, "b": math.pi / 2, "singular": True, "exact": -math.pi / 2 * math.log(2)},
]


def adaptive_simpson(f, a, b, tol=1e-10, max_depth=50):
    """(integral, evaluations)."""
    count = [0]

    def F(x):
        count[0] += 1
        return f(x)

    def rec(a, b, fa, fm, fb, whole, tol, depth):
        m = (a + b) / 2
        lm, rm = (a + m) / 2, (m + b) / 2
        flm, frm = F(lm), F(rm)
        left = (m - a) / 6 * (fa + 4 * flm + fm)
        right = (b - m) / 6 * (fm + 4 * frm + fb)
        if depth >= max_depth or abs(left + right - whole) <= 15 * tol:
            return left + right + (left + right - whole) / 15
        return rec(a, m, fa, flm, fm, left, tol / 2, depth + 1) + rec(m, b, fm, frm, fb, right, tol / 2, depth + 1)

    fa, fm, fb = F(a), F((a + b) / 2), F(b)
    whole = (b - a) / 6 * (fa + 4 * fm + fb)
    return rec(a, b, fa, fm, fb, whole, tol, 0), count[0]


def _safe(g, lo, hi):
    def h(t):
        try:
            v = g(t)
        except (ZeroDivisionError, ValueError, OverflowError):
            v = math.nan
        if math.isfinite(v):
            return v
        t2 = t + 1e-12 if abs(t - lo) <= abs(t - hi) else t - 1e-12
        return g(t2)
    return h


def _half_line(f, a):
    def g(t):
        return f(a + t / (1 - t)) / (1 - t) ** 2
    return g


def transformed(spec):
    """Pieces (g, lo, hi) with smooth, finite integrands."""
    f, a, b = spec["f"], spec["a"], spec["b"]
    if math.isinf(a) and math.isinf(b):
        pieces = [(_half_line(f, 0.0), 0.0, 1.0), (_half_line(lambda x: f(-x), 0.0), 0.0, 1.0)]
    elif math.isinf(b):
        pieces = [(_half_line(f, a), 0.0, 1.0)]
    elif spec["singular"]:
        pieces = [(lambda t: 2 * t * f(a + t * t), 0.0, math.sqrt(b - a))]
    else:
        pieces = [(f, a, b)]
    return [(_safe(g, lo, hi), lo, hi) for g, lo, hi in pieces]


def integrate(spec, tol=1e-10):
    """(value, evaluations)."""
    total, evals = 0.0, 0
    for g, lo, hi in transformed(spec):
        v, n = adaptive_simpson(g, lo, hi, tol)
        total += v
        evals += n
    return total, evals


def report():
    """(name, value, error, evaluations) per integral."""
    out = []
    for spec in INTEGRALS:
        v, n = integrate(spec)
        out.append((spec["name"], v, abs(v - spec["exact"]), n))
    return out
