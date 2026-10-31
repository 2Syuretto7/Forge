# Catastrophic cancellation, and formulas that avoid it

Subtracting nearly equal numbers keeps only the digits where they differ (Section 3). Each function below has a naive form that subtracts nearly equal quantities and a stable form that does not.

- `one_minus_cos(x)`: naive `1 - np.cos(x)`; stable $2\sin^2(x/2)$. Return `(naive, stable)`.
- `expm1_over_x(x)`: naive $(e^x - 1)/x$; stable `np.expm1(x) / x`. Return `(naive, stable)`.
- `small_root(a, b, c)`: the root of smaller magnitude of $ax^2 + bx + c$ with $b \ne 0$ and real roots. Naively it is $\frac{-b + \operatorname{sign}(b)\sqrt{b^2 - 4ac}}{2a}$, which subtracts nearly equal numbers when $b^2 \gg 4ac$; stably, compute the large root $q/a$ with $q = -\frac12\big(b + \operatorname{sign}(b)\sqrt{b^2 - 4ac}\big)$, which adds numbers of the same sign, and return $c/q$. Return `(naive, stable)`.

## Hints

1. $1 - \cos x = 2\sin^2(x/2)$ is an identity, so the stable form is exact in exact arithmetic.
2. `np.expm1` computes $e^x - 1$ without forming $e^x$ first.
3. The product of the roots is $c/a$: once you have the large root accurately, divide.
