import numpy as np


# provided
def coordinate_ascent(X, y, C, epochs, rng):
    n = len(y)
    alpha = np.zeros(n)
    w = np.zeros(X.shape[1])
    sq = np.sum(X * X, axis=1)
    for _ in range(epochs):
        for i in rng.permutation(n):
            G = y[i] * (w @ X[i]) - 1
            new = min(max(alpha[i] - G / sq[i], 0.0), C)
            if new != alpha[i]:
                w += (new - alpha[i]) * y[i] * X[i]
                alpha[i] = new
    return alpha, w


def categories(alpha, C, tol=1e-6):
    """0: alpha = 0, 1: strictly between, 2: alpha = C."""
    a = np.asarray(alpha)
    return np.where(a <= tol, 0, np.where(a >= C - tol, 2, 1))


def margin_values(w, X, y):
    """y_i w^T x_i."""
    return y * (X @ w)


def slackness_violations(alpha, w, X, y, C, tol=1e-4):
    """Points whose category disagrees with their margin value."""
    cat = categories(alpha, C)
    m = margin_values(w, X, y)
    bad = ((cat == 0) & (m < 1 - tol)) | ((cat == 1) & (np.abs(m - 1) > tol)) | ((cat == 2) & (m > 1 + tol))
    return int(np.sum(bad))


def refit_on_support(X, y, alpha, C, epochs, rng):
    """Solve again on the support vectors only."""
    s = alpha > 0
    return coordinate_ascent(X[s], y[s], C, epochs, rng)[1]
