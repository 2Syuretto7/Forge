# A one-in-a-million event: the best proposal

Estimate $P = P(Z > a)$ for a standard normal $Z$ with $a = 4.7534$, where $P \approx 10^{-6}$. A naive sampler needs about $10^8$ draws for a 10 percent error bar. Importance sampling from $N(\theta, 1)$ uses the weight $w(x) = e^{-\theta x + \theta^2/2}$, and the estimator's second moment has a closed form,

$$
m(\theta) = \mathbb{E}_q\big[(1_{x > a}\,w)^2\big] = e^{\theta^2}\,Q(a + \theta), \qquad Q(x) = P(Z > x) .
$$

- `upper_tail(x)`: $Q(x) = \frac12\operatorname{erfc}(x/\sqrt2)$.
- `second_moment(theta, a)` and `d_second_moment(theta, a)`, its derivative $2\theta e^{\theta^2}Q(a + \theta) - e^{\theta^2}\varphi(a + \theta)$, where $\varphi$ is the standard normal density.
- `best_shift(a)`: the $\theta$ in $[0, 2a]$ where the derivative vanishes, by bisection (the derivative is negative at 0 and positive at $2a$).
- `relative_error(theta, a, n)`: the relative standard error $\sqrt{(m(\theta)/P^2 - 1)/n}$; with $\theta = 0$ it is the naive sampler's.

The tests run a **gradient check** of `d_second_moment`, find the best shift a little beyond $a$, and compare the samples each method needs for a 10 percent error bar.

## Hints

1. `math.erfc` is accurate far into the tail, where `1 - erf` would round to 0.
2. Sixty halvings of $[0, 2a]$ pin the shift to machine precision.
3. Samples for relative error $r$: $n = (m/P^2 - 1)/r^2$.
