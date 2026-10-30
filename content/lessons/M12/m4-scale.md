# Scale: twenty polynomial fits on 10,000 points

Fit polynomials of degree 1 to 20 to 10,000 points by both methods, and watch the normal equations fall apart around degree 8 while QR holds on.

::::predict{id=p4 kind=choice answer=d}
You fit a degree-15 polynomial with columns $1, x, \dots, x^{15}$ on $[0, 1]$, by the normal equations in double precision. The data are exact values of a known degree-15 polynomial. How many correct digits do the computed coefficients have?

- All 16: the data are exact.
- About 10.
- About 5.
- Essentially none: the coefficients can be off by more than their own size.

:::reveal
Essentially none. With $\kappa(A) \approx 10^{11}$, the normal equations face $\kappa^2 \approx 10^{22}$, far beyond the $10^{16}$ that double precision can resolve. The fitted curve may still look reasonable, because many very different coefficient vectors give nearly the same values on $[0, 1]$, which is exactly what ill-conditioning means.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::
