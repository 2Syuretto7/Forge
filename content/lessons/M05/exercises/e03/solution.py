def sigma(f, lo, hi):
    """Sum of f(k) for k = lo..hi inclusive; 0 when hi < lo."""
    return sum(f(k) for k in range(lo, hi + 1))


def shift_index(f, lo, hi, s):
    """The same sum with the index shifted by s."""
    return sigma(lambda j: f(j - s), lo + s, hi + s)


def split(f, lo, mid, hi):
    """(sum from lo to mid, sum from mid + 1 to hi)."""
    return sigma(f, lo, mid), sigma(f, mid + 1, hi)
