# Derivation: multiple integrals and change of variables

## 1. Double integrals and Fubini

Cover a region of the plane with small rectangles of area $\Delta A$ and sum $f$ times the area: the limit is the **double integral** $\iint_R f\,dA$, the volume under the surface $z = f(x, y)$. **Fubini's theorem** says that for a continuous $f$ on a rectangle (or an absolutely integrable $f$ on any region) it can be computed as an iterated integral, in either order:

$$
\iint_{[a,b] \times [c,d]} f\,dA = \int_a^b \left( \int_c^d f(x, y)\,dy \right) dx .
$$

For a region that is not a rectangle, the inner limits depend on the outer variable.

::::derivation{id=d1 title="Iterated integrals"}
:::step
$\iint_{[0,1] \times [0,2]} xy\,dA = \int_0^1 x\,dx \cdot \int_0^2 y\,dy = \frac12 \cdot 2 =$ [[1]].
:::
:::step
The triangle $0 \leq y \leq x \leq 1$ has area $\int_0^1 \left(\int_0^x dy\right) dx = \int_0^1 x\,dx =$ [[1/2]].
:::
::::

## 2. Change of variables

Let $T$ map a region $D$ of the $(u, v)$ plane onto a region $R$ of the $(x, y)$ plane, invertibly and smoothly. A tiny rectangle $du \times dv$ at $(u, v)$ goes to a tiny curved shape that is, to first order, the parallelogram spanned by $\frac{\partial T}{\partial u}du$ and $\frac{\partial T}{\partial v}dv$: the columns of the Jacobian $J_T$, scaled. Its area is $|\det J_T|\,du\,dv$ (M10). Summing over the tiles,

$$
\iint_R f(x, y)\,dx\,dy = \iint_D f(T(u, v))\,|\det J_T(u, v)|\,du\,dv .
$$

In one dimension this is substitution, $dx = |g'(t)|\,dt$. In $n$ dimensions it is the same formula with an $n \times n$ Jacobian.

The widget's linear map multiplies every area by $|ad - bc|$, the special case where the Jacobian is the same everywhere.

:::widget{name=MatrixTransform a=1.5 b=0.5 c=0.3 d=1}
:::

## 3. Polar and spherical coordinates

For polar coordinates $x = r\cos\theta$, $y = r\sin\theta$:

::::derivation{id=d2 title="The polar Jacobian"}
:::step
$J = \begin{pmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{pmatrix}$, so $\det J = r\cos^2\theta + r\sin^2\theta =$ [[r]].
:::
:::step
The area of a disc of radius $R$ is $\int_0^{2\pi}\!\int_0^R r\,dr\,d\theta =$ [[pi*R^2]].
:::
::::

Spherical coordinates $x = r\sin\phi\cos\theta$, $y = r\sin\phi\sin\theta$, $z = r\cos\phi$ (with $\phi$ the angle from the $z$ axis) have $|\det J| = r^2\sin\phi$, which gives the volume of a ball, $\frac43\pi R^3$, and the surface of a sphere, $4\pi R^2$.

## 4. Densities under maps

If $X$ has density $p_X$ and $Y = g(X)$ with $g$ invertible, the probability of a tiny region is conserved: $p_Y(y)\,|dy| = p_X(x)\,|dx|$. In $n$ dimensions $|dy| = |\det J_g(x)|\,|dx|$, so

$$
p_Y(y) = \frac{p_X(x)}{|\det J_g(x)|} = p_X(g^{-1}(y))\,\big|\det J_{g^{-1}}(y)\big| .
$$

Where the map stretches, the density thins; where it compresses, the density piles up. If $g$ is not one to one, sum over all the preimages of $y$.

::::predict{id=p3 kind=choice answer=c}
$X$ is uniform on $[0, 1]$, density 1. What is the density of $Y = 2X$?

- 2 on $[0, 2]$.
- 1 on $[0, 2]$.
- $\frac12$ on $[0, 2]$.
- 1 on $[0, 1]$ and 0 elsewhere.

:::reveal
$\frac12$ on $[0, 2]$: the same total probability over twice the length. A density of 2 on $[0, 2]$ would integrate to 4. The factor is $1/|g'| = 1/2$, the one-dimensional Jacobian.
:::
::::

::::derivation{id=d3 title="Transforming densities"}
:::step
$X$ uniform on $[0, 1]$ and $Y = X^2$: $g^{-1}(y) = \sqrt y$ with derivative $\frac{1}{2\sqrt y}$, so $p_Y(y) = \frac{1}{2\sqrt y}$, and $p_Y(0.25) =$ [[1]].
:::
:::step
$Y = -\ln X$ has $g^{-1}(y) = e^{-y}$, so $p_Y(y) = e^{-y}$: an exponential distribution. Its density at $y = 1$ is [[e^(-1)]].
:::
::::

**Box-Muller.** Two independent uniforms $(U_1, U_2)$ map to $R = \sqrt{-2\ln U_1}$, $\Theta = 2\pi U_2$, and then $(X, Y) = (R\cos\Theta, R\sin\Theta)$. The Jacobian determinant of the whole map has absolute value $2\pi/U_1 = 2\pi e^{(X^2 + Y^2)/2}$, so the density of $(X, Y)$ is $\frac{1}{2\pi}e^{-(x^2 + y^2)/2}$: two independent standard normals from two uniforms.

## 5. Gaussians in n dimensions

By Fubini, $\int_{\mathbb{R}^n} e^{-\|x\|^2/2}\,dx = \left(\int e^{-t^2/2}\,dt\right)^n = (2\pi)^{n/2}$. For a covariance matrix $\Sigma = LL^\top$, the map $x = Lz$ from standard normals has $|\det J| = |\det L| = \sqrt{\det\Sigma}$, so the density of $x$ is

$$
p(x) = \frac{1}{(2\pi)^{n/2}\sqrt{\det\Sigma}} \exp\left(-\tfrac12 x^\top\Sigma^{-1}x\right) .
$$

::::derivation{id=d4 title="Normalizers"}
:::step
In three dimensions $\int e^{-\|x\|^2/2}\,dx =$ [[(2*pi)^(3/2)]].
:::
:::step
For $\Sigma = \operatorname{diag}(4, 9)$, $\sqrt{\det \Sigma} =$ [[6]], and the normalizer is $2\pi \cdot 6 = 12\pi$.
:::
::::

## 6. Balls in high dimensions

The unit ball in $\mathbb{R}^n$ has volume $V_n = \frac{\pi^{n/2}}{\Gamma(n/2 + 1)}$ (the Gaussian integral computed two ways, in Cartesian and in spherical coordinates, gives it). It peaks at $n = 5$ and then falls to zero, while the cube $[-1, 1]^n$ around it has volume $2^n$.

::::derivation{id=d5 title="A vanishing ball"}
:::step
$V_3 = \frac{\pi^{3/2}}{\Gamma(5/2)} =$ [[4*pi/3]].
:::
:::step
$V_{10} = \pi^5/120 \approx 2.55$, so the ball fills a fraction $V_{10}/2^{10} \approx$ [[0.0025|tol=0.0001]] of its cube.
:::
::::

:::edge{to=M23 text="the multivariate Gaussian as a linear map of standard normals."}
:::

:::edge{to=M37 text="flows and diffusion models move densities through maps, tracking Jacobian determinants."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Fubini | double integral = iterated integrals | compute areas and volumes |
| Change of variables | multiply by $\lvert\det J\rvert$ | polar, spherical, any map |
| Polar, spherical | $r$, $r^2\sin\phi$ | discs, balls, radial functions |
| Densities | $p_Y = p_X / \lvert\det J_g\rvert$ | samplers, flows |
| Box-Muller | two uniforms to two normals | Gaussian sampling |
| Gaussian normalizer | $(2\pi)^{n/2}\sqrt{\det\Sigma}$ | multivariate normal |
| Ball volume | $\pi^{n/2}/\Gamma(n/2 + 1)$, vanishes | high-dimensional geometry |
