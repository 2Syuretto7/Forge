# Limits by experiment

- `approach(f, a, side, steps=12)`: the values $f(a \pm 10^{-k})$ for $k = 1, \dots,$ `steps`, from the right (`side=+1`) or the left (`side=-1`).
- `estimate_limit(f, a, tol=1e-6)`: approach from both sides with `steps=8`; if the last values from the two sides agree within `tol` (relative to `max(1, |value|)`), return their average; otherwise return `None`.

A table of values is evidence, not proof (M03): it can be fooled, and the tests include one function that fools it at small steps. But it is the right first look.

## Hints

1. `[f(a + side * 10.0 ** -k) for k in range(1, steps + 1)]`.
2. $\sin(x)/x \to 1$ and $(1 + x)^{1/x} \to e$ at 0, while the step function has different one-sided limits.
3. Stop at $k = 8$: beyond it, rounding starts to dominate expressions like $(1 + x)^{1/x}$.
