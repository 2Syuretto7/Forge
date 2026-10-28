# Break it: a synchronization every step

Model a training loop in which the CPU needs `cpu_s` seconds to issue a step's kernels and the GPU needs `gpu_s` seconds to run them.

1. `pipelined_time(steps, cpu_s, gpu_s)`: without synchronization the CPU issues step $i + 1$ while the GPU runs step $i$; the first step costs both, and each later step the larger of the two.
2. `synced_time(steps, cpu_s, gpu_s)`: with a `.item()` at the end of every step, nothing overlaps.
3. `sync_slowdown(steps, cpu_s, gpu_s)`: the ratio of the two.

## Hints

1. `cpu_s + gpu_s + (steps - 1) * max(cpu_s, gpu_s)`.
2. The slowdown approaches $(c + g)/\max(c, g)$ for many steps: at most 2, when the two are equal.
3. Logging every 100 steps makes the synchronization cost negligible.
