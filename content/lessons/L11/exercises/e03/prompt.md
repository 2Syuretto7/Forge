# Tiling a matrix product

Model an $n \times n \times n$ product computed in $T \times T$ output blocks, each of which streams a $T$-wide strip of $A$ and of $B$ ($nT$ values each) and writes its block of $C$.

1. `tiled_matmul_bytes(n, tile, bytes_per=2)`: total device-memory traffic.
2. `min_tile_for_compute_bound(peak, bw, bytes_per=2)`: the smallest power-of-two tile whose intensity $T/b$ reaches the ridge point.
3. `tile_smem_bytes(tile, bytes_per=2)`: shared memory to hold one $T \times T$ tile of $A$ and one of $B$.

`tiled_intensity(n, tile, bytes_per)` (given) divides $2n^3$ by your traffic. Compare it with $T/b$, and the shared memory a compute-bound tile would need with the T4's 64 KB per SM.

## Hints

1. There are $(n/T)^2$ blocks.
2. Add the $n^2$ values written to $C$ once.
3. Double the tile until it is large enough.
