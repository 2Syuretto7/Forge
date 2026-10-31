# Derivation: gradient methods, momentum and noise

## 1. Gradient descent on smooth convex functions

$f$ is **$L$-smooth** when its gradient changes no faster than $L$: $\lVert\nabla f(x) - \nabla f(y)\rVert \le L\lVert x - y\rVert$. Integrating along the segment gives a quadratic upper bound,

$$
f(y) \le f(x) + \nabla f(x)^\top(y - x) + \frac L2\lVert y - x\rVert^2 ,
$$

and putting the gradient step $y = x - \frac1L\nabla f(x)$ into it gives the **descent lemma**:

$$
f\big(x - \tfrac1L\nabla f(x)\big) \le f(x) - \frac{1}{2L}\lVert\nabla f(x)\rVert^2 .
$$

Every step decreases the loss in proportion to the squared gradient. Combined with convexity (the tangent-plane inequality of M28) and a telescoping sum, it gives the **sublinear rate** $f(x_k) - f^\star \le \frac{L\lVert x_0 - x^\star\rVert^2}{2k}$. If $f$ is also $\mu$-strongly convex, $\lVert\nabla f\rVert^2 \ge 2\mu(f - f^\star)$, and the descent lemma turns into a **linear rate**: $f(x_{k+1}) - f^\star \le (1 - \mu/L)(f(x_k) - f^\star)$, an error shrinking like a geometric sequence (M05).

:::edge{from=M05 text="geometric series return as linear convergence rates."}
:::

:::edge{from=M16 text="the second-order Taylor term returns as the step-size limit 2/L."}
:::

::::derivation{id=d1 title="Two guarantees"}
:::step
With $L = 4$ and $\lVert\nabla f(x)\rVert^2 = 8$, one step of size $1/L$ lowers $f$ by at least [[1]].
:::
:::step
On a convex function with $L = 2$ and $\lVert x_0 - x^\star\rVert^2 = 10$, after 100 steps the gap to the optimum is at most [[0.1]].
:::
::::

## 2. Momentum on a quadratic

**Heavy ball** adds the previous step: $x_{k+1} = x_k - \alpha\nabla f(x_k) + \beta(x_k - x_{k-1})$. On $\frac12 x^\top Ax$ every eigenvector of $A$ evolves on its own, and along curvature $\lambda$ the error obeys the two-term recurrence

$$
\begin{pmatrix} e_{k+1} \\ e_k \end{pmatrix} = \begin{pmatrix} 1 + \beta - \alpha\lambda & -\beta \\ 1 & 0 \end{pmatrix}\begin{pmatrix} e_k \\ e_{k-1} \end{pmatrix} .
$$

Its decay rate is the spectral radius of the 2 by 2 matrix (M13). When the matrix's eigenvalues are complex, a conjugate pair, their product is $\beta$, so both have modulus exactly $\sqrt\beta$, whatever $\lambda$ is. The best constants make that happen for every curvature in $[\mu, L]$ at once, with the smallest possible $\beta$:

$$
\alpha^\star = \frac{4}{(\sqrt L + \sqrt\mu)^2}, \qquad \beta^\star = \left(\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}\right)^2, \qquad \rho = \sqrt{\beta^\star} = \frac{\sqrt\kappa - 1}{\sqrt\kappa + 1} .
$$

The step count now grows like $\sqrt\kappa$. **Nesterov's method** evaluates the gradient at the look-ahead point $x_k + \beta(x_k - x_{k-1})$; with $\alpha = 1/L$ and $\beta = \frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}$ it contracts by $1 - 1/\sqrt\kappa$ per step, and unlike heavy ball it keeps that guarantee on every smooth strongly convex function, not only quadratics.

:::edge{from=M13 text="eigenvalues of the Hessian set momentum's optimal value."}
:::

::::derivation{id=d2 title="Momentum at condition number 100"}
:::step
The optimal momentum is $(9/11)^2 \approx$ [[0.669|tol=0.002]].
:::
:::step
The error shrinks by $9/11$ per step, so a millionfold reduction takes $\ln 10^6/\ln(11/9) \approx$ [[69|tol=1]] steps.
:::
::::

## 3. Stochastic gradients and the noise floor

A training loss is an average over examples, $f(x) = \frac1n\sum_i f_i(x)$, and **stochastic gradient descent** replaces its gradient by the average over a random minibatch of $B$ examples. That estimate is unbiased, and by M24 its variance is $\sigma^2/B$, where $\sigma^2$ is the variance of one example's gradient.

On the quadratic $\frac\mu2 x^2$ with gradient noise of variance $\sigma^2/B$, one step gives

$$
\mathbb{E}x_{k+1}^2 = (1 - \eta\mu)^2\,\mathbb{E}x_k^2 + \eta^2\frac{\sigma^2}{B} ,
$$

and the error settles at the fixed point, the **noise floor**

$$
\mathbb{E}x_\infty^2 = \frac{\eta\sigma^2}{B\mu(2 - \eta\mu)} \approx \frac{\eta\sigma^2}{2B\mu} .
$$

The pull toward the minimum is proportional to $\eta$, the injected noise to $\eta^2$, so their balance is proportional to $\eta$. A constant step never reaches the minimum; the iterates wander in a stationary cloud around it, a Markov chain with a stationary distribution (M32).

:::edge{to=M32 text="constant-step SGD is a Markov chain with a stationary distribution."}
:::

::::derivation{id=d3 title="The size of the cloud"}
:::step
With $\eta = 0.1$, $\mu = 1$, $\sigma^2 = 1$ and $B = 1$, the stationary mean squared error is $0.1/1.9 \approx$ [[0.0526|tol=0.0005]].
:::
:::step
With a batch of 4 instead, it is about [[0.0132|tol=0.0003]].
:::
::::

::::predict{id=p3 kind=choice answer=a}
You halve the step size of constant-step SGD and run until the loss stops improving. How does the final plateau compare?

- Its excess over the optimum is about halved.
- Its excess is about quartered.
- It is unchanged: the plateau is set by the data.
- It is higher: smaller steps make less progress.

:::reveal
About halved: the noise floor is proportional to $\eta$. Smaller steps get there more slowly but sit closer to the minimum. That is why learning rates are decayed during training, and why a plateau that drops when the step is halved was noise, not convergence.
:::
::::

## 4. Schedules

To converge, the step must shrink: the **Robbins-Monro** conditions $\sum_k\eta_k = \infty$ (the steps can still travel any distance) and $\sum_k\eta_k^2 < \infty$ (the total injected noise is finite). The inverse-time schedule $\eta_k = \eta_0 k_0/(k + k_0)$ satisfies both and, on a strongly convex problem with $\eta_0\mu > 1$, gives an error falling like $1/k$: slower than the linear rate without noise, and the best possible with noisy gradients. Practice uses step decay, cosine decay to zero, and a short **warm-up** at the start, while the curvature is unknown and large.

:::edge{to=L05 text="proved rates meet the practical optimizers: warm-up, cosine schedules and AdamW."}
:::

## 5. Adam and its bias correction

**Adam** keeps exponential moving averages of the gradient and of its elementwise square,

$$
m_t = \beta_1 m_{t-1} + (1 - \beta_1)g_t, \qquad v_t = \beta_2 v_{t-1} + (1 - \beta_2)g_t^2 ,
$$

and steps by $\alpha\,\hat m_t/(\sqrt{\hat v_t} + \varepsilon)$: per coordinate, the mean gradient over its root mean square, so every coordinate moves about $\alpha$ when the gradient is steady, whatever its scale. Both averages start at 0, so early on they are biased toward 0: for a stationary gradient, $\mathbb{E}m_t = (1 - \beta_1^t)\,\mathbb{E}g$, because the weights $(1 - \beta_1)\beta_1^{t - s}$ sum to $1 - \beta_1^t$, a geometric series. Dividing by that sum removes the bias: $\hat m_t = m_t/(1 - \beta_1^t)$ and $\hat v_t = v_t/(1 - \beta_2^t)$.

::::derivation{id=d4 title="The first step"}
:::step
At $t = 1$ with $\beta_1 = 0.9$, the first moment's correction factor is $1/(1 - 0.9) =$ [[10]].
:::
:::step
Without correction the first step is $\alpha\frac{0.1\,g}{\sqrt{0.001}\,\lvert g\rvert}$, about [[3.16|tol=0.01]] times $\alpha$: the second moment's bias is the larger one.
:::
::::

## 6. Measuring a rate

A linear rate is a straight line on a log plot: $\log e_k \approx \log C + k\log\rho$. A least-squares fit of $\log e_k$ against $k$, over a window that skips the transient and stops before rounding noise, measures $\rho$. Sublinear rates are straight on a log-log plot: $e_k \approx Ck^{-p}$ gives slope $-p$ in $\log k$.

::::derivation{id=d5 title="Slopes"}
:::step
A rate of $0.9$ per step is a line with slope $\log_{10}0.9 \approx$ [[-0.0458|tol=0.0005]] decades per step.
:::
::::

:::edge{to=M35 text="nonlinear least squares for power-law fits."}
:::

:::edge{to=M36 text="policy gradients: stochastic gradients with high variance."}
:::

## Summary

| Method | Rate on a $\kappa$-conditioned problem | Notes |
| --- | --- | --- |
| Gradient descent, step $1/L$ | $1 - 1/\kappa$ | descent lemma; $L/(2k)$ without strong convexity |
| Gradient descent, best step | $\frac{\kappa - 1}{\kappa + 1}$ | steps $\propto \kappa$ |
| Heavy ball | $\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}$ on quadratics | $\beta^\star = \rho^2$ |
| Nesterov | $1 - 1/\sqrt\kappa$ | any smooth strongly convex $f$ |
| Constant-step SGD | stalls at $\approx \eta\sigma^2/(2B\mu)$ | noise floor $\propto \eta/B$ |
| SGD, $\eta_k \propto 1/k$ | error $\propto 1/k$ | Robbins-Monro |
| Adam | about $\alpha$ per coordinate per step | bias correction $1/(1 - \beta^t)$ |
