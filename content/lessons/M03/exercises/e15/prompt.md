# Swapping quantifiers

On the finite domain $\{0, 1, \dots, n - 1\}$, a relation is a set of pairs `(x, y)`.

- `forall_exists(rel, n)`: for every $x$ there is a $y$ with $(x, y)$ in `rel`.
- `exists_forall(rel, n)`: there is a $y$ with $(x, y)$ in `rel` for every $x$.
- `swap_counterexample(n)`: a relation (a set of pairs) on $\{0, \dots, n - 1\}$, for $n \geq 2$, where `forall_exists` is true and `exists_forall` is false.
- `smallest_counterexample()`: the smallest $n$ for which such a relation exists. Think about $n = 1$ before you answer.

## Hints

1. With `rel` a set, test membership with `(x, y) in rel`.
2. "Each $x$ is related to itself": every $x$ has a $y$, but no single $y$ serves all $x$ when there are two or more.
3. With one element, $\forall x\, \exists y$ and $\exists y\, \forall x$ say the same thing.
