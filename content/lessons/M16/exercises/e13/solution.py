def newton_orbit(f, df, x0, n):
    """Plain Newton iterates."""
    xs = [float(x0)]
    for _ in range(n):
        x = xs[-1]
        xs.append(x - f(x) / df(x))
    return xs


def cycle_length(orbit, tol=1e-9):
    """Smallest period of the tail, or None."""
    for q in range(1, 11):
        if len(orbit) >= 2 * q + 1 and all(abs(orbit[-k] - orbit[-k - q]) <= tol for k in range(1, q + 1)):
            return q
    return None


def damped_newton(f, df, x0, max_iter=100):
    """Newton with step halving until |f| decreases."""
    x = float(x0)
    for _ in range(max_iter):
        fx = f(x)
        if fx == 0:
            return x
        step = fx / df(x)
        t = 1.0
        for _ in range(50):
            if abs(f(x - t * step)) < abs(fx):
                break
            t /= 2
        x -= t * step
        if abs(t * step) < 1e-15 * max(1.0, abs(x)):
            break
    return x
