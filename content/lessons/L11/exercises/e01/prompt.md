# Counting FLOPs and bytes

Return `(flops, bytes)` for each operation, counting the minimum traffic: every input read once and every output written once, at `bytes_per` bytes per number.

1. `matmul_cost(m, n, k, bytes_per=2)`: $C = AB$ with $A$ of shape $(m, k)$ and $B$ of shape $(k, n)$; a multiply-add counts as 2 FLOPs.
2. `elementwise_cost(n_elems, flops_per_elem, n_inputs, bytes_per=2)`: reads `n_inputs` arrays and writes one.
3. `softmax_cost(rows, cols, bytes_per=2)`: 5 FLOPs per element; the input is read once and the output written once.

`intensity(cost)` (given) divides the two.

## Hints

1. The matmul reads $mk + kn$ values and writes $mn$.
2. Each output value of $C$ is a dot product of length $k$: $k$ multiplies and $k$ adds.
3. Check: a square fp16 matmul has intensity $n/3$.
