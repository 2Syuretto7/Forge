import numpy as np


def blocked_row_sums(x, block, masked=True):
    """Sum each row of x by loading `block` columns at a time from a buffer laid out like device
    memory: the rows end to end, followed by unrelated data (here: 1000.0). With masked=True,
    positions past the end of the row count as 0; without the mask they read whatever follows."""
    rows, cols = x.shape
    memory = np.concatenate([x.ravel(), np.full(rows * cols + block, 1000.0)])
    out = np.zeros(rows)
    for r in range(rows):
        for s in range(0, cols, block):
            offs = r * cols + s + np.arange(block)
            vals = memory[offs]
            if masked:
                vals = np.where(s + np.arange(block) < cols, vals, 0.0)
            out[r] += vals.sum()
    return out


def programs_needed(n, block):
    """Number of program instances for n elements: ceil(n / block)."""
    return -(-n // block)
