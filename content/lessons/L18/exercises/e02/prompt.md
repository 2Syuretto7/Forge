# Ring all-reduce

Simulate the ring all-reduce that data parallelism uses to sum gradients. `xs` holds one array per rank, $P$ ranks in a ring.

Implement `ring_allreduce(xs)`: split every array into $P$ chunks with `np.array_split`. **Reduce-scatter**: in step $s = 0, \dots, P-2$, every rank $r$ sends its chunk $(r - s) \bmod P$ to rank $r + 1$, which adds it to its own copy. Afterwards each rank holds one fully summed chunk. **All-gather**: in step $s$, rank $r$ sends its chunk $(r + 1 - s) \bmod P$ to rank $r + 1$, which replaces its own. All messages of a step are sent at once. Return the $P$ resulting arrays and the number of elements rank 0 sent.

## Hints

1. Build every step's messages from the state at the start of the step, then deliver them.
2. After reduce-scatter, rank $r$ holds the complete sum of chunk $(r + 1) \bmod P$.
3. Each rank sends $2(P-1)$ chunks of $n/P$ elements: $2(P-1)n/P$, almost independent of $P$. That is why the ring is bandwidth-optimal.
