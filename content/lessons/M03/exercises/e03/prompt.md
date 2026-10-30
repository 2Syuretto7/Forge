# Quantifiers over finite sets

Over a finite domain, quantifiers become loops.

- `for_all(pred, xs)`: `True` when `pred(x)` holds for every `x` in `xs` (and for an empty `xs`).
- `exists(pred, xs)`: `True` when `pred(x)` holds for at least one `x`.
- `for_all_exists(rel, xs, ys)`: $\forall x \in xs\ \exists y \in ys$: `rel(x, y)`.
- `exists_for_all(rel, xs, ys)`: $\exists y \in ys\ \forall x \in xs$: `rel(x, y)`.

Write the loops yourself; Python's `all` and `any` do the same job, and you may use them once your loops work.

The tests check an **invariant**: for random predicates, not `for_all(p)` equals `exists(not p)`, and `exists_for_all` implies `for_all_exists`.

## Hints

1. `for_all` returns `False` at the first failure; after the loop, `True`.
2. `for_all_exists(rel, xs, ys)` is `for_all(lambda x: exists(lambda y: rel(x, y), ys), xs)`.
3. Swap the two loops for `exists_for_all`.
