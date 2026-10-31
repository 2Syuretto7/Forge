import numpy as np


def bias_variance(degree, n, sigma, x0, trials=4000, seed=0):
    rng = np.random.default_rng(seed)
    f0 = np.sin(np.pi * x0)
    preds = np.empty(trials)
    errs = np.empty(trials)
    v0 = np.vander(np.array([x0]), degree + 1, increasing=True)[0]
    for t in range(trials):
        x = rng.uniform(-1, 1, n)
        y = np.sin(np.pi * x) + sigma * rng.normal(size=n)
        c = np.linalg.lstsq(np.vander(x, degree + 1, increasing=True), y, rcond=None)[0]
        preds[t] = v0 @ c
        y0 = f0 + sigma * rng.normal()
        errs[t] = (y0 - preds[t]) ** 2
    return {
        "bias2": float((f0 - preds.mean()) ** 2),
        "variance": float(preds.var()),
        "noise": sigma ** 2,
        "expected_error": float(errs.mean()),
    }
