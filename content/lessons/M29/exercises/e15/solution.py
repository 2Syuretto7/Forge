def heavy_ball_errors(lam, alpha, beta, iters):
    """|x_k| of heavy ball on (lam/2) x^2."""
    x = prev = 1.0
    out = [abs(x)]
    for _ in range(iters):
        x, prev = x - alpha * lam * x + beta * (x - prev), x
        out.append(abs(x))
    return out


def stable(lam, alpha, beta):
    """Stability condition of heavy ball along curvature lam."""
    return 0 < alpha * lam < 2 * (1 + beta) and 0 <= beta < 1
