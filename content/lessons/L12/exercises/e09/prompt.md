# Block sizes that fit

1. `flash_smem_bytes(block_m, block_n, d, bytes_per=2)`: on-chip bytes of one FlashAttention program, counting the $Q$, $K$ and $V$ tiles in the input precision and fp32 accumulators for the output ($B_m \times d$) and the scores ($B_m \times B_n$).
2. `best_blocks(d, budget, sizes=(16, 32, 64, 128), bytes_per=2)`: the largest square block size from `sizes` that fits the budget, or `None`.

## Hints

1. $(B_m d + 2 B_n d) \cdot \text{bytes} + 4 (B_m d + B_m B_n)$.
2. Doubling $d$ roughly halves the block that fits.
3. Real kernels also keep values in registers and use software pipelining that needs extra buffers; treat this count as a lower bound.
