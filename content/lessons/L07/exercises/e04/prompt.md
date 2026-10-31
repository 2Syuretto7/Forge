# Peak FLOPs and occupancy

1. `peak_flops(sms, cores_per_sm, clock_hz, flops_per_core_cycle=2)`.
2. `blocks_per_sm(threads_per_block, regs_per_thread, smem_per_block, lim=TURING)`: how many blocks fit on one SM at once, the smallest of: the block limit, the warp limit (`max_warps // warps_per_block`), the register limit (`registers // (regs_per_thread * threads in whole warps)`) and, if the block uses shared memory, the shared-memory limit.
3. `occupancy(...)`: resident warps divided by the maximum warps per SM.

`TURING` holds the per-SM limits of the T4's architecture.

## Hints

1. Warps per block round up: `-(-threads // 32)`.
2. Registers are allocated per warp, so count `warps * 32` threads.
3. Skip the shared-memory limit when the block uses none (division by zero).
