import numpy as np


# provided
def _softmax(z):
    p = np.exp(z - z.max())
    return p / p.sum()


# provided
def _ln(x):
    m = x - x.mean()
    s = np.sqrt(np.mean(m * m) + 1e-5)
    return m / s


# provided
def _ln_jac(x):
    n = x.size
    m = x - x.mean()
    s = np.sqrt(np.mean(m * m) + 1e-5)
    C = np.eye(n) - 1.0 / n
    return C / s - np.outer(m, m) @ C / (n * s ** 3)


# provided
def _ln_jac_wrong(x):
    m = x - x.mean()
    s = np.sqrt(np.mean(m * m) + 1e-5)
    return np.eye(x.size) / s - np.outer(m, m) / (x.size * s ** 3)


_rng = np.random.default_rng(42)
_A = _rng.normal(size=(3, 4))
_S = _rng.normal(size=(4, 4))
_W = _rng.normal(size=(5, 4))

# provided
SUITE = [
    ("tanh", np.tanh, lambda x: np.diag(1 - np.tanh(x) ** 2), 4, False),
    ("sigmoid", lambda x: 1 / (1 + np.exp(-x)), lambda x: np.diag(np.exp(-x) / (1 + np.exp(-x)) ** 2), 4, False),
    ("softplus", lambda x: np.logaddexp(0, x), lambda x: np.diag(1 / (1 + np.exp(-x))), 4, False),
    ("exp", np.exp, lambda x: np.diag(np.exp(x)), 3, False),
    ("log", np.log, lambda x: np.diag(1 / x), 3, True),
    ("sqrt", np.sqrt, lambda x: np.diag(0.5 / np.sqrt(x)), 3, True),
    ("linear", lambda x: _A @ x, lambda x: _A, 4, False),
    ("affine", lambda x: _A @ x + 1.0, lambda x: _A, 4, False),
    ("sum of squares", lambda x: np.array([x @ x]), lambda x: 2 * x[None, :], 5, False),
    ("quadratic form", lambda x: np.array([0.5 * x @ _S @ x]), lambda x: (_S @ x)[None, :], 4, False),
    ("log-sum-exp", lambda x: np.array([np.log(np.sum(np.exp(x)))]), lambda x: _softmax(x)[None, :], 5, False),
    ("softmax", _softmax, lambda x: np.diag(_softmax(x)), 4, False),
    ("normalize", lambda x: x / np.linalg.norm(x), lambda x: (np.eye(x.size) - np.outer(x, x)) / np.linalg.norm(x), 3, False),
    ("polar to cartesian", lambda v: np.array([v[0] * np.cos(v[1]), v[0] * np.sin(v[1])]), lambda v: np.array([[np.cos(v[1]), -v[0] * np.sin(v[1])], [np.sin(v[1]), v[0] * np.cos(v[1])]]), 2, False),
    ("cartesian to polar", lambda v: np.array([np.hypot(v[0], v[1]), np.arctan2(v[1], v[0])]), lambda v: np.array([[v[0], v[1]], [-v[1], v[0]]]) / np.array([[np.hypot(*v)], [v @ v]]), 2, False),
    ("product", lambda x: np.array([np.prod(x)]), lambda x: np.array([[np.prod(np.delete(x, i)) for i in range(x.size)]]), 4, False),
    ("cross product", lambda x: np.cross(x[:3], x[3:]), lambda x: np.hstack([-np.array([[0, -x[5], x[4]], [x[5], 0, -x[3]], [-x[4], x[3], 0]]), np.array([[0, -x[2], x[1]], [x[2], 0, -x[0]], [-x[1], x[0], 0]])]), 6, False),
    ("layer norm", _ln, _ln_jac, 5, False),
    ("layer norm, mean term dropped", _ln, _ln_jac_wrong, 5, False),
    ("tanh layer", lambda x: np.tanh(_W @ x), lambda x: (1 - np.tanh(_W @ x) ** 2)[:, None] * _W, 4, False),
    ("x sin y", lambda v: np.array([v[0] * np.sin(v[1])]), lambda v: np.array([[np.sin(v[1]), v[0] * np.cos(v[1])]]), 2, False),
    ("rotation by first input", lambda v: np.array([np.cos(v[0]) * v[1] - np.sin(v[0]) * v[2], np.sin(v[0]) * v[1] + np.cos(v[0]) * v[2]]), lambda v: np.array([[-np.sin(v[0]) * v[1] - np.cos(v[0]) * v[2], np.cos(v[0]), -np.sin(v[0])], [np.cos(v[0]) * v[1] - np.sin(v[0]) * v[2], np.sin(v[0]), np.cos(v[0])]]), 3, False),
    ("square elementwise", lambda x: x ** 2, lambda x: np.diag(x), 4, False),
    ("gelu tanh approximation", lambda x: 0.5 * x * (1 + np.tanh(0.7978845608 * (x + 0.044715 * x ** 3))), lambda x: np.diag(0.5 * (1 + np.tanh(0.7978845608 * (x + 0.044715 * x ** 3))) + 0.5 * x * (1 - np.tanh(0.7978845608 * (x + 0.044715 * x ** 3)) ** 2) * 0.7978845608 * (1 + 3 * 0.044715 * x ** 2)), 4, False),
    ("log of 1 + x^2", lambda x: np.log1p(x ** 2), lambda x: np.diag(2 * x / (1 + x ** 2)), 4, False),
]


def numerical_jacobian(f, x):
    """Central differences with scaled steps."""
    x = np.array(x, dtype=float)
    m = np.asarray(f(x)).size
    J = np.zeros((m, x.size))
    for j in range(x.size):
        h = np.finfo(float).eps ** (1 / 3) * max(1.0, abs(x[j]))
        e = np.zeros_like(x)
        e[j] = h
        J[:, j] = (np.asarray(f(x + e)) - np.asarray(f(x - e))) / (2 * h)
    return J


def relative_error(A, B):
    """Frobenius relative error."""
    A, B = np.asarray(A, dtype=float), np.asarray(B, dtype=float)
    return float(np.linalg.norm(A - B) / max(np.linalg.norm(A) + np.linalg.norm(B), 1e-12))


def check(entry, points=5, seed=0):
    """Worst relative error over random points."""
    name, f, jac, n, positive = entry
    rng = np.random.default_rng(seed)
    worst = 0.0
    for _ in range(points):
        x = rng.uniform(0.5, 2.0, size=n) if positive else rng.normal(size=n)
        worst = max(worst, relative_error(np.atleast_2d(jac(x)), numerical_jacobian(f, x)))
    return worst


def run_suite(tol=1e-6):
    """Names whose Jacobian disagrees."""
    return sorted(e[0] for e in SUITE if check(e) > tol)
