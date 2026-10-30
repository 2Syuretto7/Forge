# The forgotten branch

$Y = X^2$ for a standard normal $X$ is not one to one: both $\sqrt y$ and $-\sqrt y$ map to $y$.

- `one_branch(y)`: $p_X(\sqrt y)\,\frac{1}{2\sqrt y}$, only the positive preimage.
- `chi_square_1(y)`: the sum over both preimages, $\frac{2\,p_X(\sqrt y)}{2\sqrt y} = \frac{e^{-y/2}}{\sqrt{2\pi y}}$.
- `total_half_open(density, upper=60.0, n=200_000)`: $\int_0^{\text{upper}}$ by substituting $y = t^2$ (M17) to remove the $1/\sqrt y$ singularity: $\int_0^{\sqrt{\text{upper}}} \text{density}(t^2)\,2t\,dt$, midpoint rule.

`one_branch` integrates to $\frac12$; `chi_square_1` to 1.

## Hints

1. $p_X(x) = e^{-x^2/2}/\sqrt{2\pi}$.
2. After the substitution, the integrand $2t \cdot \frac{e^{-t^2/2}}{\sqrt{2\pi}\,t}$ is smooth.
3. Midpoints never evaluate at $t = 0$.
