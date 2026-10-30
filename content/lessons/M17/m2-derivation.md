# Derivation: integrals and the fundamental theorem

## 1. Riemann sums and the definite integral

Cut $[a, b]$ into $n$ strips of width $h = (b - a)/n$, pick a point $x_k$ in each, and add the rectangles:

$$
S_n = \sum_{k=1}^{n} f(x_k)\, h .
$$

If $S_n$ approaches the same limit however the points are chosen as $h \to 0$, that limit is the **definite integral** $\int_a^b f(x)\,dx$. Continuous functions on a closed interval are always integrable, and so are functions with finitely many jumps. Where $f$ is negative the area counts negatively.

::::derivation{id=d1 title="A Riemann sum by hand"}
:::step
For $\int_0^1 x^2\,dx$ with right endpoints, $S_n = \sum_{k=1}^n (k/n)^2 \cdot \frac1n = \frac{(n + 1)(2n + 1)}{6n^2}$. For $n = 10$ this is [[0.385]].
:::
:::step
As $n \to \infty$, $\frac{(n + 1)(2n + 1)}{6n^2} \to$ [[1/3]].
:::
::::

## 2. The fundamental theorem of calculus

Let $F(x) = \int_a^x f(t)\,dt$, the area accumulated up to $x$. Adding a thin strip from $x$ to $x + h$ adds an area between $h \min f$ and $h \max f$ over that strip, so

$$
\frac{F(x + h) - F(x)}{h} = \frac1h \int_x^{x + h} f(t)\,dt \to f(x)
$$

when $f$ is continuous. So $F' = f$: **accumulation is the inverse of differentiation**. If $G$ is any other function with $G' = f$, then $(G - F)' = 0$, so $G - F$ is constant (the mean value theorem, M16), and

$$
\int_a^b f(x)\,dx = G(b) - G(a) .
$$

Any **antiderivative** computes any definite integral.

::::predict{id=p3 kind=choice answer=b}
What is $\frac{d}{dx} \int_0^x e^{-t^2}\,dt$?

- 0, because the integral is a constant.
- $e^{-x^2}$.
- $-2x e^{-x^2}$.
- It has no formula, since $e^{-t^2}$ has no elementary antiderivative.

:::reveal
$e^{-x^2}$, directly from the fundamental theorem: the rate at which area accumulates is the height of the curve. The antiderivative has no formula in terms of elementary functions, yet its derivative is perfectly known. This function, scaled, is the error function behind the normal distribution's probabilities.
:::
::::

::::derivation{id=d2 title="Integrals from antiderivatives"}
:::step
$\int_0^\pi \sin x\,dx = [-\cos x]_0^\pi = 1 + 1 =$ [[2]].
:::
:::step
The puzzle: an antiderivative of $6x - 6x^2$ is $3x^2 - 2x^3$, so $\int_{0.2}^{0.3} 6x(1 - x)\,dx =$ [[0.112]].
:::
::::

## 3. Substitution and integration by parts

Read the chain rule backwards: since $\frac{d}{dx} F(g(x)) = f(g(x))\,g'(x)$,

$$
\int f(g(x))\,g'(x)\,dx = \int f(u)\,du, \qquad u = g(x) .
$$

Read the product rule backwards: since $(uv)' = u'v + uv'$,

$$
\int_a^b u v'\,dx = [uv]_a^b - \int_a^b u' v\,dx .
$$

::::derivation{id=d3 title="Substitution and parts"}
:::step
With $u = x^2$, $\int 2x\cos(x^2)\,dx = \sin(x^2) + C$, so $\int_0^{\sqrt\pi} 2x\cos(x^2)\,dx = \sin\pi - \sin 0 =$ [[0]].
:::
:::step
With $u = x$ and $v' = e^x$, $\int_0^1 x e^x\,dx = [x e^x]_0^1 - \int_0^1 e^x\,dx = e - (e - 1) =$ [[1]].
:::
::::

## 4. Improper integrals

An infinite interval or an integrand that blows up is handled by a limit: $\int_1^\infty f = \lim_{R \to \infty} \int_1^R f$ and $\int_0^1 f = \lim_{\epsilon \to 0} \int_\epsilon^1 f$, when the limits exist. Powers decide most cases: $\int_1^\infty x^{-p}\,dx$ is finite exactly when $p > 1$, and $\int_0^1 x^{-p}\,dx$ exactly when $p < 1$. The **integral test** compares $\sum 1/k^p$ with $\int x^{-p}$: they converge or diverge together, which is why the harmonic series of M05 diverges like $\ln n$.

::::derivation{id=d4 title="Two improper integrals"}
:::step
$\int_1^R x^{-2}\,dx = 1 - 1/R$, so $\int_1^\infty x^{-2}\,dx =$ [[1]].
:::
:::step
$\int_\epsilon^1 x^{-1/2}\,dx = 2 - 2\sqrt\epsilon$, so $\int_0^1 \frac{dx}{\sqrt x} =$ [[2]], although the integrand is infinite at 0.
:::
::::

## 5. The Gaussian integral

$I = \int_{-\infty}^\infty e^{-x^2}\,dx$ has no antiderivative to evaluate, but its square can be computed. Write $I^2$ as a double integral over the plane and switch to polar coordinates, where the small area element is $r\,dr\,d\theta$ (a thin ring of radius $r$; M20 derives this factor in general):

$$
I^2 = \int\!\!\int e^{-(x^2 + y^2)}\,dx\,dy = \int_0^{2\pi}\!\!\int_0^\infty e^{-r^2}\, r\,dr\,d\theta .
$$

::::derivation{id=d5 title="Squaring the Gaussian integral"}
:::step
The inner integral is $\left[-\tfrac12 e^{-r^2}\right]_0^\infty = \tfrac12$, so $I^2 = 2\pi \cdot \tfrac12 =$ [[pi]].
:::
:::step
So $I = \sqrt\pi$, and substituting $x = t/\sqrt 2$, $\int e^{-t^2/2}\,dt =$ [[sqrt(2*pi)]]: the normalizing constant of the standard normal density.
:::
::::

## 6. Quadrature: computing integrals numerically

Most integrals in practice have no closed form. **Quadrature** rules approximate them from a few values of $f$:

- **Trapezoid**: replace $f$ on each strip by a straight line. Error about $\frac{(b - a)h^2}{12}|f''|$: halving $h$ divides it by 4.
- **Simpson**: replace $f$ on each pair of strips by a parabola, weights $\frac{h}{3}(1, 4, 2, 4, \dots, 4, 1)$. Error about $\frac{(b - a)h^4}{180}|f''''|$: halving $h$ divides it by 16.
- **Adaptive Simpson**: compare Simpson on an interval with Simpson on its two halves. Where they agree to the tolerance, accept; where not, split and recurse. Evaluations concentrate where $f$ is difficult. It can be fooled: a feature narrower than its first few sample points is never seen.

All of these assume smoothness. At a singularity, a jump or fast oscillation, their error estimates lie, which Movement 5 shows.

:::edge{to=M20 text="integrals over the plane, and the Jacobian factor r of polar coordinates, derived in general."}
:::

:::edge{to=M22 text="expectations and variances of continuous random variables are integrals against a density."}
:::

:::edge{to=M24 text="Monte Carlo: random samples instead of a grid, with an error that ignores the dimension."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Integral | limit of Riemann sums | areas, totals, probabilities |
| Fundamental theorem | $F' = f$; $\int_a^b f = G(b) - G(a)$ | integrate by antiderivative |
| Substitution | chain rule backwards | change of variable |
| Parts | product rule backwards | products of functions |
| Improper | limit of integrals; $x^{-p}$ test | tails and singularities |
| Gaussian | $\int e^{-x^2} = \sqrt\pi$ | normalize the normal |
| Quadrature | trapezoid $h^2$, Simpson $h^4$, adaptive | numbers when no formula exists |
