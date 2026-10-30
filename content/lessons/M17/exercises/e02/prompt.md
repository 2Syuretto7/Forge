# Simpson's rule

- `simpson(f, a, b, n)`: composite Simpson with an even number `n` of strips: $\frac h3\big(f_0 + 4f_1 + 2f_2 + 4f_3 + \dots + 4f_{n-1} + f_n\big)$. Raise `ValueError` for odd `n`.
- `simpson_error_ratio(f, a, b, exact, n)`: the error with `n` strips over the error with `2n`, about 16 for smooth `f`.

Simpson's rule integrates every cubic exactly, one degree more than its parabolas suggest.

## Hints

1. Build the weights with `w = np.ones(n + 1); w[1:-1:2] = 4; w[2:-1:2] = 2`.
2. `np.linspace(a, b, n + 1)` for the points.
3. Test on $x^3$: the error is 0 up to rounding.
