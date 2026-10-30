# Dividing by something that can be zero

The equation $x^2 = kx$ has two solutions for any $k \neq 0$. Write two solvers and compare them.

- `solve_by_factoring(k)`: bring everything to one side, $x(x - k) = 0$, and use the zero-product rule. Return the sorted list of distinct solutions (one solution when $k = 0$).
- `solve_by_dividing(k)`: the tempting method. Divide both sides by $x$ and return the list of what is left, `[k]`.
- `lost_solutions(k)`: the sorted list of solutions the dividing method misses.
- `is_solution(k, x)`: whether $x$ satisfies $x^2 = kx$ exactly.

## Hints

1. A product is zero exactly when a factor is zero: $x = 0$ or $x = k$.
2. `sorted(set([0, k]))` handles $k = 0$.
3. `[x for x in factoring if x not in dividing]`.
