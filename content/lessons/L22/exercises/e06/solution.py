import math


def pages_needed(tokens, block):
    """Fixed-size pages of `block` token slots needed for a sequence."""
    return math.ceil(tokens / block)


def paged_waste(lengths, block):
    """Unused token slots when every sequence gets whole pages."""
    return sum(pages_needed(n, block) * block - n for n in lengths)


def contiguous_waste(lengths, max_len):
    """Unused token slots when every sequence reserves max_len slots up front."""
    return sum(max_len - n for n in lengths)
