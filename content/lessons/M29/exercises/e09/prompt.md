# Adam from scratch

Adam keeps exponential moving averages of the gradient and of its square, corrects their bias toward the zero start, and steps by their ratio (Section 6):

$$
m_t = \beta_1 m_{t-1} + (1 - \beta_1)g_t, \quad v_t = \beta_2 v_{t-1} + (1 - \beta_2)g_t^2, \quad \hat m_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat v_t = \frac{v_t}{1 - \beta_2^t},
$$

$$
x_t = x_{t-1} - \alpha\frac{\hat m_t}{\sqrt{\hat v_t} + \varepsilon} .
$$

- `adam(grad, x0, lr, iters, b1=0.9, b2=0.999, eps=1e-8, bias_correction=True)`: return the list of iterates, starting from $t = 1$.
- `adam_moments(gs, b1=0.9, b2=0.999)`: for a sequence of gradients, the arrays of corrected $\hat m_t$ and $\hat v_t$.

The tests check that the corrected moments of a constant gradient equal it exactly at every step, that each Adam step on a constant gradient has length close to $\alpha$ per coordinate whatever the gradient's scale, and that Adam handles a quadratic whose coordinates are scaled by a factor of $10^4$.

## Hints

1. Keep $m$ and $v$ as arrays of the parameter's shape, starting at zero.
2. $1 - \beta^t$ with $t$ starting at 1.
3. Per-coordinate normalization by $\sqrt{\hat v}$ makes Adam insensitive to the scale of each coordinate.
