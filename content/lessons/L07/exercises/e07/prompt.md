# Launch overhead

1. `step_time(kernels, peak, bw, launch_s=10e-6)`: `kernels` is a list of `(flops, bytes)`. They run one after another; each costs the larger of its roofline time (`kernel_time`, given) and the launch overhead, because the GPU cannot start a kernel before the CPU has issued it.
2. `launch_bound_fraction(kernels, peak, bw, launch_s=10e-6)`: the fraction of kernels whose GPU time is below the launch overhead.

Then compare one elementwise kernel on $2^{24}$ values with the same work split into 4096 kernels of 4096 values.

## Hints

1. Use `max(kernel_time(f, b, peak, bw), launch_s)` per kernel.
2. On a T4, a 4096-element fp16 kernel moves 24 KB, under a tenth of a microsecond of memory time.
3. The split version does the same FLOPs and bytes in total.
