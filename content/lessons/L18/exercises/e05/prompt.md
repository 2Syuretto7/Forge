# ZeRO stage 1

Plain data parallelism keeps a full copy of the Adam states on every rank. ZeRO stage 1 shards them: rank $r$ owns a contiguous slice of the parameters, keeps $m$ and $v$ only for that slice, updates only that slice, and the updated slices are gathered.

1. `adam_update(w, g, m, v, t, lr, b1=0.9, b2=0.999, eps=1e-8)`: one bias-corrected Adam step.
2. `zero1_step(w, rank_grads, states, t, lr)`: average the ranks' gradients; rank $r$ updates the indices `np.array_split(np.arange(len(w)), P)[r]` with its state `states[r] = (m, v)`; return the gathered weights and the new states.

## Hints

1. Adam is elementwise, so updating slices separately gives exactly the same result as one full update.
2. In a real system the averaging is a reduce-scatter (each rank only needs its slice of the averaged gradient) and the gathering an all-gather: the same traffic as one all-reduce.
3. Each rank stores $1/P$ of the optimizer state: $12/P$ instead of 12 bytes per parameter.
