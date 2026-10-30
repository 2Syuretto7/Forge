def sigma(f, lo, hi):
    """Sum of f(k) for k = lo..hi inclusive; 0 when hi < lo."""
    raise NotImplementedError


def shift_index(f, lo, hi, s):
    """The same sum with the index shifted by s."""
    raise NotImplementedError


def split(f, lo, mid, hi):
    """(sum from lo to mid, sum from mid + 1 to hi)."""
    raise NotImplementedError
