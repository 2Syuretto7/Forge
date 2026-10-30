# Newton's method gone wrong

- `newton_orbit(f, df, x0, n)`: the first `n + 1` iterates of Newton's method, without any stopping rule.
- `cycle_length(orbit, tol=1e-9)`: the smallest period $q$ from 1 to 10 such that the last $2q$ iterates repeat with period $q$ (each equals the one $q$ steps before it, within `tol`), or `None`.
- `damped_newton(f, df, x0, max_iter=100)`: Newton with **backtracking**: halve the step until $|f|$ decreases (at most 50 halvings); return the final `x`.

The tests run plain Newton on $x^3 - 2x + 2$ from 0 (a cycle of period 2) and on the cube root (which diverges), and show the damped version converging from 0 to the real root near $-1.769$.

## Hints

1. A fixed point of the iteration is a cycle of period 1.
2. Compare `orbit[-k]` with `orbit[-k - q]` for `k` from 1 to `q`.
3. Damping trades speed for safety far from the root and keeps the full step near it.
