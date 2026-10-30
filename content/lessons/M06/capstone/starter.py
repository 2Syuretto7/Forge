import numpy as np

LAWS = [
    ("exponential", {"a": 2.0, "b": 1.3}),
    ("power", {"a": 5.0, "p": 1.7}),
    ("linear", {"a": 10.0, "b": 3.0}),
    ("power", {"a": 0.5, "p": 3.0}),
    ("exponential", {"a": 100.0, "b": 0.85}),
    ("linear", {"a": 200.0, "b": -4.0}),
]


# provided
def make_datasets(seed=0):
    """Six (x, y) datasets with about 3 percent multiplicative noise."""
    rng = np.random.default_rng(seed)
    out = []
    for law, prm in LAWS:
        x = np.linspace(1, 30, 40)
        if law == "linear":
            y = prm["a"] + prm["b"] * x
        elif law == "exponential":
            y = prm["a"] * prm["b"] ** x
        else:
            y = prm["a"] * x ** prm["p"]
        out.append((x, y * np.exp(rng.normal(scale=0.03, size=x.size))))
    return out


def fit_line(u, v):
    """(slope, intercept, r2) of the least-squares line."""
    raise NotImplementedError


def classify(x, y):
    """The law whose coordinates make the data straightest."""
    raise NotImplementedError


def estimate(x, y, law):
    """Parameters of the law fitted to the data."""
    raise NotImplementedError


def detect(datasets):
    """[(law, params)] for each dataset."""
    raise NotImplementedError
