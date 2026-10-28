# IO complexity

Count elements moved between device memory and the chip:

1. `standard_io(N, d)`: unfused attention reads $Q, K, V$ and writes $O$ ($4Nd$), and writes and reads both the scores and the probabilities ($4N^2$).
2. `flash_io(N, d, M)`: FlashAttention with on-chip memory of $M$ elements: about $N^2 d^2 / M + 4Nd$.
3. `io_ratio(N, d, M)`: standard over flash.

Evaluate the ratio for $d = 64$ and $M$ = 25,000 elements (about 100 KB in fp32) at $N = 1024$ and $4096$.

## Hints

1. Use floating-point division in `flash_io`.
2. The ratio grows with $N$ until $N^2$ dominates both terms, then levels off near $4M/d^2$.
3. FlashAttention performs slightly more FLOPs than standard attention, and is still faster: bytes, not FLOPs, set the time.
