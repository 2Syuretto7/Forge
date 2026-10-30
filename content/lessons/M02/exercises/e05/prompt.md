# Solve a linear equation, all three cases

Write `solve_linear(a, b, c)` for the equation $a x + b = c$:

- if $a \neq 0$, return the solution $x = (c - b)/a$ as a float;
- if $a = 0$ and $b = c$, every $x$ works: return the string `"all"`;
- if $a = 0$ and $b \neq c$, no $x$ works: return `None`.

Then write `utilization(hours, n_params, n_tokens, peak_flops)`: a run of $6ND$ FLOPs took `hours` GPU-hours on a GPU with the given peak. Solve $\text{hours} = \dfrac{6ND}{\text{peak} \cdot u \cdot 3600}$ for the utilization $u$. This is M01's estimate turned around: the formula becomes an equation and the unknown moves.

## Hints

1. Test `a == 0` first.
2. Multiply both sides by $u$ and divide by hours: $u = \dfrac{6ND}{\text{peak} \cdot 3600 \cdot \text{hours}}$.
3. The tests check that the utilization you find reproduces the hours.
