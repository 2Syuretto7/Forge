# IsoFLOP profiles

Hoffmann et al.'s second method trains several model sizes at each of a few fixed compute budgets. Each budget gives a U-shaped curve of loss against model size, whose minimum is that budget's best size.

1. `isoflop_minimum(N, L)`: fit a parabola to $L$ against $\log N$ and return the size at its vertex and the loss there.
2. `allocation_exponent(C, N_opt)`: the exponent $a$ in $N_\text{opt} = k\,C^a$, fitted in log-log coordinates.

## Hints

1. `np.polyfit(np.log(N), L, 2)` returns $(c_2, c_1, c_0)$; the vertex is at $\log N = -c_1 / 2c_2$.
2. Return $N = e^{x}$, not $x$.
3. The parabola only approximates the curve near its minimum, so place the sizes around the expected optimum.
