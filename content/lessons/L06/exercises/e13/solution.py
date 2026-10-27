import numpy as np


def learning_curve(sizes, degree, sigma=0.3, trials=200, seed=0):
    rng = np.random.default_rng(seed)
    grid = np.linspace(-1, 1, 200)
    G = np.vander(grid, degree + 1, increasing=True)
    f = np.sin(np.pi * grid)
    out = []
    for n in sizes:
        errs = []
        for _ in range(trials):
            x = rng.uniform(-1, 1, n)
            y = np.sin(np.pi * x) + sigma * rng.normal(size=n)
            c = np.linalg.lstsq(np.vander(x, degree + 1, increasing=True), y, rcond=None)[0]
            errs.append(np.mean((G @ c - f) ** 2))
        out.append(np.mean(errs))
    return np.array(out)
