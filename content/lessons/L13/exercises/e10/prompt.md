# Predicting the speedup

1. `amdahl_speedup(fractions, speedups)`: the overall speedup when parts of a run that take the given fractions of the original time are sped up by the given factors.
2. `t4_part_speedups()`: the speedup bounds on a T4 for matrix products (fp32 cores to fp16 tensor cores) and for memory-bound operations (half the bytes).

If 70 percent of a step is matrix products and 30 percent memory-bound work, what speedup can mixed precision give at most? Compare it with what the capstone measures.

## Hints

1. New time $= \sum_i f_i / s_i$; the speedup is its inverse.
2. The memory-bound part limits the result: even infinitely fast matrix products leave $0.3/2$.
3. Real tensor-core kernels reach well below their peak, so measured speedups are lower than this bound.
