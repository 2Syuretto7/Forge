# Two equations, two unknowns

Write `solve_2x2(a, b, c, d, p, q)` for the system

$$
\begin{aligned}
a x + b y &= p \\
c x + d y &= q
\end{aligned}
$$

by elimination: compute the determinant $ad - bc$; if it is exactly zero raise `ValueError`; otherwise return the pair `(x, y)` with $x = (pd - bq)/(ad - bc)$ and the matching formula for $y$ (derive it by eliminating $x$ instead).

Also write `residual(a, b, c, d, p, q, x, y)`: the larger of the two absolute errors $|ax + by - p|$ and $|cx + dy - q|$. A solver that reports its residual lets its user check it.

The tests check an **invariant**: for thousands of random systems, the residual of your solution is tiny.

## Hints

1. Eliminating $x$: multiply the first equation by $c$, the second by $a$, subtract: $(bc - ad)\,y = cp - aq$.
2. So $y = (aq - cp)/(ad - bc)$.
3. `max(abs(...), abs(...))`.
