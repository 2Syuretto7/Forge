# Derivation: stochastic differential equations and diffusion

## 1. Brownian motion and stochastic differential equations

Brownian motion $W_t$ starts at 0 and has independent increments $W_{t+h} - W_t \sim N(0, h)$: in time $h$ it moves about $\sqrt h$, the limit of M32's scaled random walk. A **stochastic differential equation**

$$
dX = a(X, t)\,dt + b(X, t)\,dW
$$

means that over a short step $X$ changes by the drift $a\,h$ plus a random kick $b\,\Delta W$ of size $\sqrt h$. The **Euler-Maruyama** method simulates it exactly that way, $X_{k+1} = X_k + a(X_k, t_k)h + b(X_k, t_k)\sqrt h\,z_k$, with an error that shrinks as the step does. Because the kicks are of order $\sqrt h$, much larger than $h$, the paths are continuous but nowhere differentiable.

## 2. The Ornstein-Uhlenbeck process

The **Ornstein-Uhlenbeck** process $dX = -\theta(X - \mu)\,dt + \sigma\,dW$ pulls toward $\mu$ and is kicked by noise. Multiply by $e^{\theta t}$ to solve it: $X_t$ given $X_0$ is Gaussian with

$$
\mathbb{E}X_t = \mu + (X_0 - \mu)e^{-\theta t}, \qquad \operatorname{Var}X_t = \frac{\sigma^2}{2\theta}\big(1 - e^{-2\theta t}\big) ,
$$

so every start is forgotten at rate $\theta$ and the process settles into $N(\mu, \sigma^2/(2\theta))$, its stationary distribution, with autocorrelation $e^{-\theta\tau}$. The forward process of a diffusion model is this with $\theta = 1$, $\mu = 0$, $\sigma = \sqrt2$:

$$
dx = -x\,dt + \sqrt2\,dW, \qquad x_t = e^{-t}x_0 + \sqrt{1 - e^{-2t}}\,\varepsilon .
$$

::::derivation{id=d1 title="What is left of the signal"}
:::step
At $t = 3$ the signal is multiplied by $e^{-3} \approx$ [[0.0498|tol=0.0005]], and the noise has variance $1 - e^{-6} \approx 0.9975$.
:::
::::

## 3. Ito's lemma

Ordinary calculus keeps terms of first order in $dt$. For a function of Brownian motion, $(dW)^2$ is of size $dt$ and must be kept: **Ito's lemma** says that for $Y = f(X)$ with $dX = a\,dt + b\,dW$,

$$
dY = \Big(f'(X)\,a + \tfrac12f''(X)\,b^2\Big)\,dt + f'(X)\,b\,dW .
$$

For $f(W) = W^2$ it gives $d(W^2) = 2W\,dW + dt$, so $\mathbb{E}W_t^2 = t$, which the ordinary rule $d(W^2) = 2W\,dW$ would put at 0. The extra term is the curvature of $f$ times the variance of the kick; it is why the probability-flow ODE of Section 7 has half the score of the reverse SDE.

::::derivation{id=d2 title="Ito's correction"}
:::step
By Ito's lemma, $\mathbb{E}W_2^2 = \mathbb{E}\int_0^2 dt =$ [[2]].
:::
::::

## 4. Scores

The **score** of a density is $s(x) = \nabla_x\log p(x)$, the direction in which the density increases fastest relative to its size. It ignores normalizing constants, which is why it is learnable when $p$ is not. For a Gaussian $N(m, v)$ it is $(m - x)/v$; for a mixture, the responsibility-weighted average of the components' scores. Langevin dynamics (M32) needs nothing else to sample $p$.

::::predict{id=p3 kind=choice answer=a}
For the noised data at a large time $t$, nearly $N(0, 1)$, what is the score at $x = 2$?

- About $-2$: it points back toward 0, with size equal to the distance.
- About $+2$.
- About 0, since the density is nearly flat.
- It depends on the data.

:::reveal
About $-2$: the score of $N(0, 1)$ is $-x$. At large $t$ everything is pulled back toward the origin; at small $t$ the score points toward the nearest concentration of data.
:::
::::

## 5. The noised data distribution

Under the forward process the density of $x_t$ is the data density shrunk by $e^{-t}$ and blurred by a Gaussian of variance $1 - e^{-2t}$. If the data are a Gaussian mixture, so is $x_t$, with means $e^{-t}m_k$ and variances $s_k^2e^{-2t} + 1 - e^{-2t}$, and its score is known exactly: the setting of this lesson's exercises, where learned scores can be checked against the truth. As $t$ grows the noised distribution approaches $N(0, 1)$, the mean's memory decaying like $e^{-t}$.

## 6. Denoising score matching

The noised data's score is unknown when the data distribution is, but it is a conditional average of something known. Given $x_0$, $x_t = ax_0 + \sigma\varepsilon$ with $a = e^{-t}$ and $\sigma = \sqrt{1 - a^2}$ is Gaussian (M23), with conditional score $\nabla\log p(x_t \mid x_0) = -\varepsilon/\sigma$. The marginal score is the average of the conditional ones over the $x_0$ that could have produced $x_t$:

$$
\nabla\log p_t(x) = \mathbb{E}\big[-\varepsilon/\sigma \,\big|\, x_t = x\big] .
$$

Since a conditional expectation minimizes squared error, the **denoising score-matching** objective

$$
\mathbb{E}_{x_0, \varepsilon}\,\big\lVert s(x_t, t) + \varepsilon/\sigma\big\rVert^2
$$

is minimized by the true score, and it needs only samples of the data and of the noise. Weighted by $\sigma^2$ and summed over noise levels, it trains a network $s_\theta(x, t)$, often written as a noise predictor $\hat\varepsilon = -\sigma s_\theta$.

::::derivation{id=d3 title="A denoising target"}
:::step
At $t = 0.5$, $\sigma = \sqrt{1 - e^{-1}} \approx 0.795$; a noise draw $\varepsilon = 0.6$ gives the target $-\varepsilon/\sigma \approx$ [[-0.755|tol=0.002]].
:::
::::

## 7. The reverse-time SDE and the probability-flow ODE

Anderson's theorem: if $dx = f(x, t)\,dt + g(t)\,dW$ has marginal densities $p_t$, then the same marginals, traversed from $t = T$ down to 0, are produced by

$$
dx = \big[f(x, t) - g(t)^2\nabla\log p_t(x)\big]\,dt + g(t)\,d\bar W ,
$$

with $dt < 0$ and $\bar W$ a Brownian motion running backwards. For our forward process, $f = -x$ and $g = \sqrt2$, so a reverse Euler-Maruyama step from $t$ to $t - h$ is

$$
x \leftarrow x + h\big(x + 2\nabla\log p_t(x)\big) + \sqrt{2h}\,z .
$$

Removing the noise and halving the score term gives the **probability-flow ODE**, $dx/dt = -x - \nabla\log p_t(x)$, a deterministic invertible map with the same marginals: noise in, data out, and densities transported by the change-of-variables rule of M20. Three practical choices follow: start at an end time $T$ large enough that $p_T \approx N(0, 1)$, take more steps where the score changes fastest (near $t = 0$), and never let the steps be so long that Euler-Maruyama becomes unstable.

:::widget{name=DiffusionStepper steps=60 T=4 frac=1}
:::

::::derivation{id=d4 title="One reverse step"}
:::step
From $x = 1$ at a time where the score is $-1$, with $h = 0.1$ and noise draw $z = 0$, the step gives $1 + 0.1(1 - 2) =$ [[0.9]].
:::
::::

## 8. Learning a score from data

With only samples of the data, one simple score model is exact for a known distribution: a kernel density estimate, each training point replaced by a Gaussian of bandwidth $h$. Noised, it is a mixture with centres $e^{-t}c_i$ and variance $h^2e^{-2t} + 1 - e^{-2t}$, so its score is computable at every time. Denoising score matching on held-out data chooses $h$. With $h = 0$ the estimate is the training set itself, the exact minimizer of the training objective, and the sampler, run to a small enough final time, reproduces training points: **memorization**. Neural score models generalize because they are smooth in the same way a bandwidth is, and memorize when trained long enough on too few examples.

::::derivation{id=d5 title="A kernel at time t"}
:::step
At $t = 1$ a kernel of bandwidth $h = 0.2$ has variance $0.04e^{-2} + 1 - e^{-2} \approx$ [[0.870|tol=0.002]].
:::
::::

:::edge{to=M38 text="diffusion models as a paper to derive and reproduce."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Euler-Maruyama | $X_{k+1} = X_k + ah + b\sqrt h\,z$ | simulating SDEs |
| Ornstein-Uhlenbeck | $x_t = e^{-t}x_0 + \sqrt{1 - e^{-2t}}\,\varepsilon$ | the forward noising process |
| Ito's lemma | $dY = (f'a + \frac12f''b^2)dt + f'b\,dW$ | calculus with noise |
| Score | $\nabla\log p$, no normalizer needed | direction toward data |
| Score matching | minimize $\mathbb{E}\lVert s(x_t) + \varepsilon/\sigma\rVert^2$ | learning scores from samples |
| Reverse SDE | $dx = [-x - 2\nabla\log p_t]dt + \sqrt2\,d\bar W$ | sampling |
| Probability-flow ODE | $dx/dt = -x - \nabla\log p_t$ | deterministic sampling, likelihoods |
