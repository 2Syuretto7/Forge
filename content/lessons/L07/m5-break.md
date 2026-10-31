# Break it: tiny kernels and needless synchronization

## Launch-bound loops

The fastest way to make a GPU slow is to give it work in tiny pieces. A Python loop over rows that calls a tensor operation per element or per row pays the launch overhead every time, and the GPU spends most of its time idle. The same happens, more mildly, in NumPy: every Python-level operation costs far more than the arithmetic it performs.

:::exercise{ref=e11}
:::

## Synchronizing every step

::::predict{id=p5 kind=choice answer=a}
A training loop logs `loss.item()` after every step. Each step needs 2 ms of CPU time to launch its kernels and 6 ms of GPU time. How much slower is the loop than one that logs only every 100 steps?

- About a third slower: 8 ms per step instead of 6.
- No slower: logging is cheap.
- Twice as slow.
- About 100 times slower.

:::reveal
Without synchronization, the CPU issues step $i + 1$ while the GPU runs step $i$, so a step costs $\max(2, 6) = 6$ ms. With `.item()` every step, the CPU waits for the GPU, then the GPU waits while the CPU issues the next step: $2 + 6 = 8$ ms. The loss is the same; only the overlap is lost. When the CPU and GPU times are close, synchronizing every step nearly doubles the time.
:::
::::

:::exercise{ref=e12}
:::

## What to take away

- Before optimizing a kernel, find out which roof it is under: memory-bound kernels need fewer bytes (fusion, lower precision), not faster arithmetic.
- Give the GPU large operations; fuse or batch small ones.
- Keep GPU values on the GPU: log them every so often, never every step.
