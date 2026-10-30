# Pascal's triangle and the binomial theorem

- `pascal_rows(n)`: the list of rows $0, 1, \dots, n$ of Pascal's triangle.
- `expand(a, b, n)`: the list of the $n + 1$ terms $\binom{n}{k} a^k b^{n-k}$ for $k = 0, \dots, n$; their sum is $(a + b)^n$.
- `poly_power(n)`: the coefficients of $(1 + x)^n$, lowest power first.

The tests check an **invariant**: each row sums to $2^n$, its alternating sum is 0 (for $n \geq 1$), and `sum(expand(a, b, n))` equals $(a + b)^n$ exactly for random integers.

## Hints

1. Build each row from the previous one, as in the previous exercise.
2. Take the coefficients from the last row of `pascal_rows(n)`.
3. The coefficients of $(1 + x)^n$ are the $n$-th row.
