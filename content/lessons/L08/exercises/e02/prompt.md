# A tiled matrix product

Implement `tiled_matmul(A, B, T)`: compute $C = AB$ in $T \times T$ output tiles. For each output tile, loop over $K$ in steps of $T$, multiply the $A$ tile by the $B$ tile and accumulate. Sizes need not be multiples of $T$ (slicing past the end of an array returns a shorter slice). Return `(C, loads)`, where `loads` counts every element read from $A$ and $B$.

Compare `loads` with the $2n^3/T$ of the derivation, and with the $2n^3$ an untiled product (one row times one column per output) would read.

## Hints

1. Three nested loops: output row tiles, output column tiles, and the reduction.
2. Add `a.size + b.size` for every pair of tiles loaded.
3. Accumulate in a small array and write it into `C` once per output tile.
