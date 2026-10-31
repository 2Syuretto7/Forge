# Break it: overflowing softmaxes and unmasked blocks

## fp16 overflow

:::exercise{ref=e11}
:::

## Block sizes that do not divide the data

Triton block sizes are powers of two; tensor sizes are whatever the model needs. A kernel that loads a full block for the last, partial block reads past the end of its row: into the next row, or past the end of the tensor into unrelated memory. Without bounds checks on a GPU this rarely crashes. It returns wrong numbers.

::::predict{id=p5 kind=choice answer=a}
A row-sum kernel uses blocks of 64 on rows of 100 values and forgets the mask. What is wrong with its output?

- Every row's sum includes 28 values that belong to the next row or to whatever follows the tensor.
- Only the last row is wrong.
- Nothing: the extra values are zeros.
- The kernel fails to compile.

:::reveal
Rows of 100 need two blocks; the second covers positions 64 to 127, of which 28 lie beyond the row. In row-major memory those are the first 28 values of the next row, and for the last row whatever follows the tensor. Every row is wrong, and nothing reports an error.
:::
::::

:::exercise{ref=e12}
:::

## What to take away

- Exponentiate after subtracting the maximum, and accumulate in fp32.
- Mask every load and store whose block can extend past the data.
- Test every kernel against a simple reference at sizes that are not multiples of the block size.
