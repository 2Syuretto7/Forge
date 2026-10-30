import numpy as np


def contour_segments(f, level, box, n):
    """Marching-squares segments of f = level."""
    xs = np.linspace(-box, box, n + 1)
    v = np.array([[f(np.array([x, y])) - level for x in xs] for y in xs])
    segs = []
    for j in range(n):
        for i in range(n):
            c = [(xs[i], xs[j]), (xs[i + 1], xs[j]), (xs[i + 1], xs[j + 1]), (xs[i], xs[j + 1])]
            val = [v[j, i], v[j, i + 1], v[j + 1, i + 1], v[j + 1, i]]
            pts = []
            for e in range(4):
                a, b = val[e], val[(e + 1) % 4]
                if (a < 0) != (b < 0):
                    t = a / (a - b)
                    p, q = c[e], c[(e + 1) % 4]
                    pts.append(np.array([p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])]))
            if len(pts) >= 2:
                segs.append((pts[0], pts[1]))
            if len(pts) == 4:
                segs.append((pts[2], pts[3]))
    return segs


def max_cosine(segments, grad):
    """Largest |cos| between a segment and the gradient at its midpoint."""
    worst = 0.0
    for p, q in segments:
        d = q - p
        g = grad((p + q) / 2)
        if np.linalg.norm(g) == 0 or np.linalg.norm(d) == 0:
            continue
        worst = max(worst, abs(d @ g) / (np.linalg.norm(d) * np.linalg.norm(g)))
    return float(worst)
