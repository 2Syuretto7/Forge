# Sequences

A sequence is a function of the whole numbers. Write four generators, each returning a Python list.

- `arithmetic(a, d, n)`: the first `n` terms $a, a + d, a + 2d, \dots$
- `geometric(a, r, n)`: the first `n` terms $a, ar, ar^2, \dots$
- `recurrence(f, x0, n)`: the first `n` terms of $x_0, f(x_0), f(f(x_0)), \dots$, where each term is `f` applied to the one before.
- `nth_arithmetic(a, d, k)`: the term with index `k` (counting from 0) of the arithmetic sequence, without building the list.

## Hints

1. `[a + d * k for k in range(n)]`.
2. In `recurrence`, start with `[x0]` and append `f(xs[-1])` until the list has `n` terms.
3. Index `k` of the arithmetic sequence is `a + k * d`.
