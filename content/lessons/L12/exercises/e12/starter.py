import numpy as np


def blocked_row_sums(x, block, masked=True):
    """Sum each row of x by loading `block` columns at a time from a buffer laid out like device
    memory: the rows end to end, followed by unrelated data (here: 1000.0). With masked=True,
    positions past the end of the row count as 0; without the mask they read whatever follows."""
    raise NotImplementedError


def programs_needed(n, block):
    """Number of program instances for n elements: ceil(n / block)."""
    raise NotImplementedError
