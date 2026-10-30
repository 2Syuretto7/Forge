# A difference quotient across a jump

The step function $H(x) = 1$ for $x > 0$ and 0 otherwise jumps at 0.

- `jump_central(h)`: the central difference of $H$ at 0 with step `h`.
- `blowup_rate(hs)`: the slope of $\log|\text{estimate}|$ against $\log h$ over the given steps (a least-squares line, as in M12). For a jump of size $J$ the central difference is $J/(2h)$, so the slope is $-1$: the "derivative" grows without bound as the step shrinks, which is how a finite-difference check exposes a discontinuity.
- `smoothed_step(x, w)`: the sigmoid $1/(1 + e^{-x/w})$, a continuous version of the step of width `w`, whose derivative at 0 is $1/(4w)$.

## Hints

1. $(H(h) - H(-h))/(2h) = 1/(2h)$.
2. `np.polyfit(np.log(hs), np.log(np.abs(vals)), 1)[0]`.
3. As $w \to 0$ the sigmoid approaches the step, and its slope at 0 grows like $1/w$: the same blow-up.
