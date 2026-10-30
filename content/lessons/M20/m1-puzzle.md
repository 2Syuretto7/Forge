# Puzzle: where do the samples crowd?

Draw points uniformly in the unit square, $(u, v)$, and send each to the plane by $r = u$, $\theta = 2\pi v$: the point at distance $u$ from the origin, at angle $2\pi v$.

::::predict{id=p1 kind=choice answer=b}
The points land in the unit disc. Are they spread evenly over it?

- Yes: a uniform input gives a uniform output.
- No: they crowd near the centre, because the small circles there get as many points as the large ones farther out.
- No: they crowd near the rim, where the circles are longer.
- They all land on one circle.

:::reveal
They crowd near the centre. Every band of radii of the same width, say $[0.1, 0.2]$ and $[0.8, 0.9]$, receives the same number of points, but the inner band has far less area. The density at radius $r$ is proportional to $1/r$. To fill the disc evenly, use $r = \sqrt u$ instead, which the widget offers.
:::
::::

::::predict{id=p2 kind=numeric answer=5 tol=0.1}
With $r = u$, how many times denser are the points at radius $0.1$ than at radius $0.5$?

:::reveal
Five times. A thin ring at radius $r$ and width $dr$ has area $2\pi r\,dr$ and receives a fraction $dr$ of the points, so the density is $\frac{1}{2\pi r}$, and $0.5/0.1 = 5$. The factor $r$ in the area of the ring is the Jacobian determinant of polar coordinates; dividing by it is the change-of-variables formula for densities.
:::
::::

The small square in the left panel maps to the curved shape on the right. Move it toward $u = 0$ and watch its image shrink; the caption compares the image's area with $|\det J|$ and reports how much denser the samples become there.

:::widget{name=JacobianWarp map=polar s=0.1 t=0.3 size=0.1}
:::

## Questions to carry into the derivation

1. How do you integrate over a region of the plane, and in which order?
2. What replaces $dx = g'(t)\,dt$ when there are two variables?
3. What happens to a probability density when its variable is transformed?
4. Why does a ball fill less and less of its cube as the dimension grows?
