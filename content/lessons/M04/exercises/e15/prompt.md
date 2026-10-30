# Fail loudly at the domain boundary

NumPy evaluates `np.sqrt` and `np.log` on whole arrays and, outside the domain, returns `nan` or `-inf` with at most a warning. A single `nan` then poisons every sum it touches.

- `silent_failures(xs)`: for a NumPy array `xs`, the indices where `np.sqrt(xs)` or `np.log(xs)` is not finite. Compute them inside `with np.errstate(all="ignore"):` so no warnings are printed.
- `poisoned_mean(xs)`: the mean of `np.log(xs)`, computed naively (it will be `nan` or `-inf` if any entry is outside the domain).
- `strict_log(xs)`: return `np.log(xs)` if every entry is positive; otherwise raise `ValueError` naming how many entries are outside the domain and the first bad index.

## Hints

1. `np.flatnonzero(~np.isfinite(a) | ~np.isfinite(b))`.
2. `np.mean(np.log(xs))` inside the same `errstate` block.
3. `bad = np.flatnonzero(xs <= 0)`; if `bad.size`, raise.
