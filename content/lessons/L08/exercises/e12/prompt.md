# Break it: a block that runs off the end

Simulate a row-sum kernel on a flat buffer laid out like device memory: the rows of `x` end to end, followed by unrelated data (the value 1000.0).

1. `blocked_row_sums(x, block, masked=True)`: for each row, load `block` consecutive positions at a time starting from the row's start, until the row is covered; with `masked=True`, zero the positions beyond the row's end before adding; without the mask, add whatever is there.
2. `programs_needed(n, block)`: how many blocks cover `n` elements.

## Hints

1. Build the buffer once: `np.concatenate([x.ravel(), np.full(rows * cols + block, 1000.0)])`.
2. Offsets of a block: `r * cols + s + np.arange(block)`; valid where `s + np.arange(block) < cols`.
3. This is what `mask=offs < n` does in every Triton load and store.
