# Antiderivatives by substitution and by parts

Write each antiderivative in closed form:

- `F1(x)`: of $x e^x$ (by parts).
- `F2(x)`: of $\ln x$ (by parts with $u = \ln x$, $v' = 1$), for $x > 0$.
- `F3(x)`: of $x\sin x$ (by parts).
- `F4(x)`: of $\frac{2x}{1 + x^2}$ (substitution $u = 1 + x^2$).
- `F5(x)`: of $\cos(x) e^{\sin x}$ (substitution $u = \sin x$).
- `definite(F, a, b)`: $F(b) - F(a)$.

The tests run a **gradient check** (each derivative, by central differences, equals the integrand) and compare `definite` with Simpson's rule.

## Hints

1. $\int x e^x\,dx = x e^x - \int e^x\,dx$.
2. $\int \ln x\,dx = x\ln x - \int x \cdot \frac1x\,dx$.
3. Any constant of integration works; the tests only differentiate and subtract.
