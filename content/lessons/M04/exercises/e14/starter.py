def brackets(f, y, lo, hi, m=1000):
    """Cells (a, b) of an m-cell grid where f - y changes sign or is zero at a."""
    raise NotImplementedError


def bisect(f, y, a, b, steps=60):
    """Root of f - y on [a, b] whose ends have opposite signs (or a zero)."""
    raise NotImplementedError


def all_preimages(f, y, lo, hi):
    """Every solution of f(x) = y in [lo, hi], sorted."""
    raise NotImplementedError
