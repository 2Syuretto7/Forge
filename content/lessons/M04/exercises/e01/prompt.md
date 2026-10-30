# Machines

Write four small machines and a helper.

- `square(x)` returns $x^2$.
- `relu(x)` returns $\max(0, x)$.
- `affine(a, b)` **returns a function**: the machine $x \mapsto ax + b$. So `affine(3, 2)(4)` is 14. Define the inner function with `def` inside `affine` and return it, or return a `lambda`.
- `apply_all(f, xs)` returns the list of outputs `[f(x) for x in xs]`.

## Hints

1. `max(0, x)`.
2. `def affine(a, b):` then `def machine(x): return a * x + b` and `return machine`.
3. The inner function remembers `a` and `b` even after `affine` has returned: that is a closure.
