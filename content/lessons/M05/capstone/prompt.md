# Capstone: a cost model of eight algorithms

The starter provides `ALGORITHMS`: eight functions of `n`, each returning a dictionary of counts, `{"ops": ...}` and, for the two matrix multiplications, `"loads"` as well. They are:

| name | algorithm | counted operation |
| --- | --- | --- |
| `sum_list` | add up a list of $n$ numbers | additions |
| `all_pairs` | compare every pair $i < j$ | comparisons |
| `all_triples` | check every triple $i < j < k$ | checks |
| `prefix_naive` | each prefix sum recomputed from scratch | additions |
| `prefix_running` | prefix sums with a running total | additions |
| `binary_search` | worst-case search in a sorted list of $n$ | comparisons |
| `matmul_naive` | $n \times n$ product, triple loop | multiply-adds; loads of entries of A and B |
| `matmul_blocked` | the same with $8 \times 8$ blocks, $n$ a multiple of 8 | multiply-adds; loads of blocks counted per entry |

Fill in:

- `FORMULAS[name](n)`: the closed form of `ops` for every algorithm, and `LOAD_FORMULAS[name](n)` for the two multiplications.
- `STEPS[name](n)`: the cost added in going from size $n$ to size $n + 1$, so that the tests can verify your formula by induction (base case at $n = 1$, step for $n = 1$ to 60). For `matmul_blocked`, whose sizes go in multiples of 8, give the step from $n$ to $n + 8$ instead.
- `predicted_ratio(name, n)`: `FORMULAS[name](2 * n) / FORMULAS[name](n)`.

The tests check every formula against the counters, the induction for each, and that the counted ratio at $n = 64$ is within 20 percent of your predicted ratio.
