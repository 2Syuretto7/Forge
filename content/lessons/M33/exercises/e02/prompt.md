# The roofline

A chip that can do $P$ flops per second and move $W$ bytes per second runs a kernel of intensity $I$ at most at $\min(P, I\cdot W)$ flops per second (Section 1). Below the **ridge point** $I^* = P/W$ the kernel waits on memory; above it, on arithmetic.

- `attainable(I, peak, bw)`: $\min(P, IW)$.
- `ridge_point(peak, bw)`: $P/W$.
- `bound(I, peak, bw)`: `"memory"` when $I < P/W$, otherwise `"compute"`.
- `time_estimate(flops, nbytes, peak, bw)`: the roofline's lower bound on the running time, $\max(\text{flops}/P, \text{bytes}/W)$.

The tests use the T4 of the Colab lessons in fp32, $8.1 \times 10^{12}$ flops per second and $320 \times 10^9$ bytes per second, the numbers the Roofline widget shows.

## Hints

1. The two terms of `time_estimate` are the time for the arithmetic alone and for the traffic alone; the slower one wins.
2. The ridge point has units of flops per byte.
3. A kernel exactly at the ridge is balanced; call it compute-bound.
