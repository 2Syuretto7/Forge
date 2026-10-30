LINES = [
    (lambda a, b: a, lambda a, b: b),
    (lambda a, b: a * a, lambda a, b: a * b),
    (lambda a, b: a * a - b * b, lambda a, b: a * b - b * b),
    (lambda a, b: (a + b) * (a - b), lambda a, b: b * (a - b)),
    (lambda a, b: a + b, lambda a, b: b),
    (lambda a, b: 2 * b, lambda a, b: b),
    (lambda a, b: 2, lambda a, b: 1),
]


def holds(line, a, b):
    """Whether the line's sides are equal at (a, b)."""
    raise NotImplementedError


def first_false_line(lines, a, b):
    """Index of the first line that is false at (a, b), or None."""
    raise NotImplementedError


def divisor_at_step(a, b):
    """What line 4 divides by: a - b."""
    raise NotImplementedError
