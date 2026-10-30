# Speed per evaluation

A method of order $p$ that needs $w$ function evaluations per step has **efficiency index** $p^{1/w}$: the order gained per evaluation.

- `efficiency(p, w)`: $p^{1/w}$.
- `evaluations_for_digits(p, w, start_digits, digits)`: the evaluations needed to grow from `start_digits` correct digits to at least `digits`, multiplying the digit count by $p$ each step (for $p > 1$).
- `bisect_evaluations(digits)`: bisection gains $\log_{10} 2$ digits per evaluation; the evaluations for `digits` digits from none, rounded up.

## Hints

1. Newton: $p = 2$, $w = 2$ ($f$ and $f'$): index $\sqrt 2 \approx 1.414$. Secant: $p = 1.618$, $w = 1$.
2. Loop: `d = start; steps = 0; while d < digits: d *= p; steps += 1`, then multiply by `w`.
3. `math.ceil(digits / math.log10(2))`.
