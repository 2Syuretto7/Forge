# Counting flops and bytes

A kernel's cost has two parts: the arithmetic it does and the data it moves (Section 1). For a matrix product $C = AB$ with $A$ of shape $m \times k$ and $B$ of shape $k \times n$, each of the $mn$ outputs takes $k$ multiplications and $k$ additions. At the least, every input is read once and every output written once.

- `matmul_flops(m, n, k)`: $2mnk$.
- `matmul_bytes(m, n, k, word=4)`: $(mk + kn + mn)\cdot$ `word`, the minimal traffic.
- `intensity(flops, nbytes)`: flops per byte.
- `matvec_intensity(m, n, word=4)`: the intensity of $y = Ax$ for $A$ of shape $m \times n$, with $2mn$ flops and $(mn + n + m)$ words.

The tests answer the puzzle's numbers: $1.374 \times 10^{11}$ flops for a 4096 matmul, an intensity near 683 in fp32, and about half a flop per byte for a large matrix-vector product, more than a thousand times less.

## Hints

1. Intensity grows with the size of a matmul, about $n/6$ for square fp32 matrices, because the work grows like $n^3$ and the data like $n^2$.
2. A matrix-vector product touches each matrix entry once for two flops, whatever its size.
3. Return plain Python numbers.
