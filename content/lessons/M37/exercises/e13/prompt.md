# Break it: a step too long

Euler-Maruyama on the Ornstein-Uhlenbeck process $dx = -\theta x\,dt + \sigma\,dW$ multiplies $x$ by $1 - \theta h$ each step. For $h > 2/\theta$ that factor exceeds 1 in size and the simulation explodes; well before that, its stationary variance is wrong (Section 2): the recursion $v = (1 - \theta h)^2v + \sigma^2h$ gives

$$
v_h = \frac{\sigma^2}{\theta(2 - \theta h)}, \quad\text{against the true } \frac{\sigma^2}{2\theta} .
$$

- `em_ou(x0, theta, sigma, h, steps, n, rng)`: final values of `n` Euler-Maruyama paths.
- `em_stationary_var(theta, sigma, h)`: $v_h$, or `math.inf` if $\theta h \ge 2$.
- `exact_ou(x0, theta, sigma, h, steps, n, rng)`: the same with exact steps (e02), for comparison.

The tests find Euler-Maruyama's variance 33 percent too large at $\theta h = 0.5$, the exact scheme right at any step, and an explosion past $\theta h = 2$.

## Hints

1. This is the SGD recursion of M32 in disguise, with $\theta$ as the curvature and $h$ as the learning rate.
2. Use `np.errstate(over="ignore")` and test with `np.isfinite`.
3. Stiff drifts need small steps, implicit schemes or exact transitions; diffusion samplers face this near $t = 0$.
