def to_bytes(text):
    """The UTF-8 bytes of text, as a list of integers 0..255."""
    raise NotImplementedError


def from_bytes(ids):
    """Decode a list of byte values back to text, replacing invalid sequences."""
    raise NotImplementedError


def count_pairs(ids, counts=None):
    """Counts of adjacent pairs, in order of first occurrence."""
    raise NotImplementedError


def merge(ids, pair, new_id):
    """Replace every non-overlapping occurrence of pair, scanning left to right, with new_id."""
    raise NotImplementedError
