# Squaring both sides of an inequality

- `squaring_keeps_order(a, b)`: for a pair with $a < b$, return whether $a^2 < b^2$.
- `find_counterexample(trials=1000, seed=0)`: draw pairs of numbers uniform in $[-10, 10]$ with `random.Random(seed)`, order each pair so the first is smaller, and return the first pair `(a, b)` with $a < b$ but $a^2 \geq b^2$; `None` if none turns up.
- `safe_to_square(a, b)`: whether $a < b$ is guaranteed to imply $a^2 < b^2$ because both numbers are non-negative.

## Hints

1. `a * a < b * b`.
2. `a, b = sorted((rnd.uniform(-10, 10), rnd.uniform(-10, 10)))`.
3. `a >= 0 and b >= 0`.
