import math


def pages_needed(tokens, block):
    """Fixed-size pages of `block` token slots needed for a sequence."""
    raise NotImplementedError


def paged_waste(lengths, block):
    """Unused token slots when every sequence gets whole pages."""
    raise NotImplementedError


def contiguous_waste(lengths, max_len):
    """Unused token slots when every sequence reserves max_len slots up front."""
    raise NotImplementedError
