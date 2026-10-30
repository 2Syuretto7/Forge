def line_through(p1, p2):
    """(m, c) of the line through two points with different x."""
    raise NotImplementedError


def misfit(points, m, c):
    """Sum of squared vertical misses of the line y = m x + c."""
    raise NotImplementedError


def best_pair_line(points):
    """The line through a pair of points with the smallest misfit on all points."""
    raise NotImplementedError
