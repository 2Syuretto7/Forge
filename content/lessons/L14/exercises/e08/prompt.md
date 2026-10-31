# Pipeline schedules

Pipeline parallelism gives each of $p$ stages a contiguous block of layers and streams $m$ micro-batches through them.

1. `gpipe_order(p, m)`: every stage runs all $m$ forward passes, then all backward passes in reverse order.
2. `one_f_one_b_order(p, m)`: stage $s$ runs $\min(p - s - 1, m)$ warm-up forwards, then alternates one forward and one backward while forwards remain, then the remaining backwards.
3. `simulate(orders, tf=1.0, tb=2.0)`: forward $j$ on stage $s$ waits for forward $j$ on stage $s - 1$; backward $j$ on stage $s$ waits for backward $j$ on stage $s + 1$ (the last stage, for its own forward $j$). Each stage runs its list in order, one op at a time. Return the finishing time and the largest number of micro-batches any stage holds between its forward and its backward.

## Hints

1. Sweep the stages repeatedly, starting each stage's next op as soon as its dependency has finished; raise an error if no stage can move.
2. Both schedules take $(m + p - 1)(t_f + t_b)$: the bubble is $(p-1)/(m + p - 1)$ of the time.
3. GPipe holds all $m$ micro-batches' activations at once; 1F1B holds at most $p$.
