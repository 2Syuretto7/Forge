import numpy as np


def _fit(x, y, d):
    return np.linalg.lstsq(np.vander(x, d + 1, increasing=True), y, rcond=None)[0]


def _pred(c, x):
    return np.vander(x, len(c), increasing=True) @ c


def curves(x_tr, y_tr, x_te, y_te, degrees):
    tr, te = [], []
    for d in degrees:
        c = _fit(x_tr, y_tr, d)
        tr.append(np.mean((_pred(c, x_tr) - y_tr) ** 2))
        te.append(np.mean((_pred(c, x_te) - y_te) ** 2))
    return np.array(tr), np.array(te)


def best_degree(degrees, test_mse):
    return int(np.asarray(degrees)[int(np.argmin(test_mse))])
