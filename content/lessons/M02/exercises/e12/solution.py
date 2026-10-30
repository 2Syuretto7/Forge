def line_through(p1, p2):
    """(m, c) of the line through two points with different x."""
    (x1, y1), (x2, y2) = p1, p2
    m = (y2 - y1) / (x2 - x1)
    return m, y1 - m * x1


def misfit(points, m, c):
    """Sum of squared vertical misses of the line y = m x + c."""
    return sum((y - (m * x + c)) ** 2 for x, y in points)


def best_pair_line(points):
    """The line through a pair of points with the smallest misfit on all points."""
    best, best_err = None, float("inf")
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if points[i][0] == points[j][0]:
                continue
            m, c = line_through(points[i], points[j])
            err = misfit(points, m, c)
            if err < best_err:
                best, best_err = (m, c), err
    return best
