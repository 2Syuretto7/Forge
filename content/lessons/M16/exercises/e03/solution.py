def newton(f, df, x0, tol=1e-14, max_iter=50):
    """(root, iterates) by Newton's method."""
    x = float(x0)
    hist = [x]
    for _ in range(max_iter):
        d = df(x)
        if d == 0:
            raise ValueError("zero derivative")
        step = f(x) / d
        x -= step
        hist.append(x)
        if abs(step) < tol * max(1.0, abs(x)):
            break
    return x, hist


def newton_sqrt(a):
    """Square root by Newton's method."""
    x0 = a if a >= 1 else 1.0
    return newton(lambda x: x * x - a, lambda x: 2 * x, x0)[0]
