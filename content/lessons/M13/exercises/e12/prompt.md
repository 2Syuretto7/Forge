# What fits and what it costs

- `dense_bytes(n)`: a dense float64 $n \times n$ matrix.
- `sparse_bytes(nnz, index_bytes=4, value_bytes=8)`: an edge list with two index arrays and one weight array.
- `iteration_flops(nnz, n)`: one sparse step: a multiply and an add per link, plus about 3 operations per page for the teleport and the residual: $2\,\text{nnz} + 3n$.
- `seconds(n, nnz, steps, flops_per_s)`: the total time of `steps` iterations at a sustained rate.

The tests size a 100,000-page graph with a million links and a web of $10^{10}$ pages with $10^{11}$ links.

## Hints

1. Integers throughout for the byte counts.
2. A web-scale iteration is $2 \times 10^{11}$ operations: memory bandwidth, not arithmetic, is the real limit there.
3. Steps times flops per step, divided by the rate.
