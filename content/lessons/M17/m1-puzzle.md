# Puzzle: a probability that is an area

A machine part's wear $X$, as a fraction of its limit, has the **density** $p(x) = 6x(1 - x)$ on $[0, 1]$: a curve with total area 1 under it. Probabilities are areas: the chance that $X$ lands in an interval is the area over that interval.

::::predict{id=p1 kind=choice answer=a}
What is the probability that $X$ equals exactly $0.25$?

- 0: a single point has no width, so it has no area.
- $p(0.25) = 1.125$.
- $1/n$ for some large $n$.
- It cannot be computed.

:::reveal
Zero. A density is not a probability; it is probability per unit length, and a point has length zero. This is why continuous probabilities are always asked about intervals, and why $p(x)$ can exceed 1, as it does here at $x = 0.5$.
:::
::::

::::predict{id=p2 kind=numeric answer=0.112 tol=0.003}
What is the probability that $X$ lands in $[0.2, 0.3]$?

:::reveal
$0.112$. The density is about 1.0 to 1.3 across the interval, so the area is a little over $0.1$; exactly, $\int_{0.2}^{0.3} 6x(1 - x)\,dx = [3x^2 - 2x^3]_{0.2}^{0.3} = 0.216 - 0.104 = 0.112$. The bracket uses an antiderivative, which Section 2 shows is always allowed.
:::
::::

Fill the interval with strips and watch the sum approach the area. Switch rules: midpoints and trapezoids are far better than left endpoints.

:::widget{name=RiemannSum f=beta rule=left n=4}
:::

## Questions to carry into the derivation

1. What exactly is "the area under a curve", for a curve that is not made of straight pieces?
2. Why does an antiderivative compute it?
3. What if the interval is infinite, or the function blows up at an end?
4. How many evaluations does it take to get eight correct digits?
