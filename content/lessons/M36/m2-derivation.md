# Derivation: score functions, gradient estimators and MDPs

## 1. The log-derivative trick

Let $J(\theta) = \mathbb{E}_{x \sim p_\theta}f(x) = \sum_xp_\theta(x)f(x)$, where $f$ need not be differentiable and $x$ may be discrete. Differentiate the probabilities, not $f$, and use $\nabla p = p\,\nabla\log p$:

$$
\nabla_\theta J = \sum_xf(x)\,\nabla_\theta p_\theta(x) = \sum_xp_\theta(x)\,f(x)\,\nabla_\theta\log p_\theta(x) = \mathbb{E}_x\big[f(x)\,\nabla_\theta\log p_\theta(x)\big] .
$$

The vector $\nabla_\theta\log p_\theta(x)$ is the **score**. The gradient is again an expectation under $p_\theta$, so an average over samples estimates it without bias (M24): the **score-function** estimator.

::::derivation{id=d1 title="The coin, by the trick"}
:::step
With $p = \frac12$, $r_1 = 3$, $r_0 = 1$ and score $x - p$, the expectation $\frac12 \cdot 3 \cdot \frac12 + \frac12 \cdot 1 \cdot (-\frac12)$ is [[0.5]], the derivative of the puzzle.
:::
::::

## 2. REINFORCE

For a softmax policy over actions, $\pi_a = \mathrm{softmax}(z)_a$, the score is $\nabla_z\log\pi_a = e_a - \pi$, the same one-hot-minus-probabilities vector as the gradient of cross-entropy (M27). Sampling $a \sim \pi$ and forming

$$
\hat g = r_a\,(e_a - \pi)
$$

gives **REINFORCE**: an unbiased estimate of $\nabla_z\mathbb{E}r_a = \pi\odot(r - \pi\cdot r)$. Read it as supervised learning on your own samples, with the label weighted by how good the outcome was: raise the log-probability of what you did, in proportion to the reward.

:::edge{to=L17 text="REINFORCE is the policy-gradient estimator behind RLHF."}
:::

## 3. Baselines and variance

The score has mean zero, $\mathbb{E}[\nabla\log\pi_a] = \nabla\sum_a\pi_a = \nabla 1 = 0$. So for any $b$ that does not depend on the sampled action,

$$
\mathbb{E}\big[(r_a - b)\,\nabla\log\pi_a\big] = \mathbb{E}\big[r_a\,\nabla\log\pi_a\big] ,
$$

and the **baseline** $b$ costs no bias. It can cost a great deal of variance or save it: the variance contains $(\bar r - b)^2\,\mathbb{E}\lVert e_a - \pi\rVert^2$, so rewards far from $b$ make every estimate large, pushing the sampled action up or down by an amount unrelated to whether it was good. The average reward is the natural baseline; in sequential problems, the state value $V(s)$. A baseline that depends on the action is a different matter: then it cannot be pulled out of the expectation, and $b(a) = cr_a$ multiplies the gradient by $1 - c$.

::::predict{id=p3 kind=choice answer=b}
Add 10 to every reward of a bandit and use REINFORCE without a baseline. What happens to the gradient estimates?

- Their mean changes, because every reward changed.
- Their mean stays the same; their variance grows many times over.
- Nothing: adding a constant changes nothing.
- They become biased toward the most likely action.

:::reveal
The mean stays the same, since the constant multiplies a score of mean zero, but the variance grows, by more than forty times in e03. With the baseline $b = \mathbb{E}r$ the shift disappears entirely.
:::
::::

::::derivation{id=d2 title="The size of a score"}
:::step
For a uniform policy over 4 actions, $\lVert e_a - \pi\rVert^2 = 1 - 2\pi_a + \lVert\pi\rVert^2 = 1 - \frac12 + \frac14 =$ [[0.75]], whichever action was sampled.
:::
::::

## 4. The reparameterization trick and Gumbel-softmax

When the sample is a differentiable function of the parameters and of noise that does not depend on them, $x = \mu + \sigma\varepsilon$ with $\varepsilon \sim N(0, 1)$, the gradient can move inside the expectation:

$$
\nabla_\mu\,\mathbb{E}f(\mu + \sigma\varepsilon) = \mathbb{E}f'(\mu + \sigma\varepsilon), \qquad \nabla_\sigma\,\mathbb{E}f(\mu + \sigma\varepsilon) = \mathbb{E}\big[f'(x)\,\varepsilon\big] .
$$

This **pathwise** estimator uses the derivative of $f$, which tells it which direction helps, where the score function only learns from $f$'s values how good a random perturbation was. Its variance is usually far smaller. For $f(x) = \lVert x\rVert^2$ and $x \sim N(0, I_d)$, the per-sample variance of the gradient in $\mu_1$ is $(d + 2)(d + 4)$ for the score function, $2d + 8$ with the baseline $\mathbb{E}f = d$, and $4$ for the pathwise estimator, whatever $d$: the score function hears all $d$ coordinates' noise through $f$, the pathwise estimator only the one that matters.

:::widget{name=EstimatorVariance maxd=256 mu=0 n=2000}
:::

::::derivation{id=d3 title="A pathwise derivative"}
:::step
For $f(x) = x^2$, $\mathbb{E}f = \mu^2 + \sigma^2$; at $\sigma = 0.7$ its derivative in $\sigma$, which $\mathbb{E}[2x\varepsilon]$ estimates, is [[1.4]].
:::
::::

Discrete samples have no pathwise derivative, but they have a reparameterization: with independent Gumbel noise $g_i = -\log(-\log u_i)$, $\arg\max_i(z_i + g_i)$ is distributed as $\mathrm{softmax}(z)$. Replacing the argmax by $\mathrm{softmax}((z + g)/\tau)$, the **Gumbel-softmax**, gives a differentiable relaxation, biased by an amount that vanishes as $\tau \to 0$ while the variance of its gradients grows.

## 5. Markov decision processes and Bellman equations

A **Markov decision process** has states $s$, actions $a$, transition probabilities $P(s' \mid s, a)$, rewards $R(s, a)$ and a discount $\gamma \in [0, 1)$. A policy $\pi(a \mid s)$ turns it into a Markov chain (M32) with transition matrix $P_\pi$ and expected reward $R_\pi$. The **return** is $G_t = \sum_{k \ge 0}\gamma^kr_{t+k}$, the **value** $V^\pi(s) = \mathbb{E}[G_t \mid s_t = s]$, and the **action value** $Q^\pi(s, a)$ the same after taking $a$ first. Conditioning on the first step gives the **Bellman equation**

$$
V^\pi = R_\pi + \gamma P_\pi V^\pi \quad\Longrightarrow\quad V^\pi = (I - \gamma P_\pi)^{-1}R_\pi ,
$$

and for the best policy the **Bellman optimality equation** $V^*(s) = \max_a[R(s, a) + \gamma\sum_{s'}P(s' \mid s, a)V^*(s')]$. Its right-hand side is a contraction with factor $\gamma$ in the maximum norm, so **value iteration**, applying it repeatedly, converges to $V^*$ from any start.

::::derivation{id=d4 title="A state that never ends"}
:::step
A state that loops to itself with reward $-1$ forever has $V = -1 + \gamma V$; with $\gamma = 0.95$, $V = -1/(1 - 0.95) =$ [[-20]].
:::
::::

## 6. The policy gradient theorem

Let $J(\theta) = \sum_s\rho_0(s)V^{\pi_\theta}(s)$. Differentiating the Bellman equation and unrolling it gives the **policy gradient theorem**:

$$
\nabla_\theta J = \sum_sd^\pi(s)\sum_a\pi(a \mid s)\,\nabla_\theta\log\pi(a \mid s)\,Q^\pi(s, a), \qquad d^\pi = \rho_0^\top(I - \gamma P_\pi)^{-1} ,
$$

where $d^\pi(s)$ counts discounted visits to $s$. The dynamics are never differentiated; they enter only through $d^\pi$ and $Q^\pi$, which episodes sample. Along one episode, $\sum_t\gamma^t(G_t - V(s_t))\nabla\log\pi(a_t \mid s_t)$ estimates it, with the returns-to-go $G_t$ standing in for $Q$ and the state value as a baseline; in practice the factor $\gamma^t$ is usually dropped, a small bias traded for weight on later steps.

## 7. Optimizing a proxy

In RLHF the reward is a learned model, right on average and wrong in places. Maximizing it alone drives the policy to wherever it is most wrong. The KL-regularized objective

$$
\max_\pi\ \mathbb{E}_\pi[\hat r] - \beta\,\mathrm{KL}(\pi\,\|\,\pi_{\text{ref}}) \qquad\text{has optimum}\qquad \pi^* \propto \pi_{\text{ref}}\,e^{\hat r/\beta}
$$

(the Gibbs form of M30), so it moves away from the reference policy only where the proxy's advantage is large compared with $\beta$. Small $\beta$ trusts the proxy completely; large $\beta$ ignores it. In between, true quality first rises and then falls as optimization pressure grows.

:::edge{to=M38 text="training on rewards: estimators, baselines and regularization."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Log-derivative trick | $\nabla\mathbb{E}f = \mathbb{E}[f\,\nabla\log p]$ | gradients through discrete samples |
| REINFORCE | $r_a(e_a - \pi)$ | policy gradients |
| Baseline | $(r_a - b)\nabla\log\pi_a$, $b$ independent of $a$ | unbiased variance reduction |
| Reparameterization | $\nabla\mathbb{E}f(\mu + \sigma\varepsilon) = \mathbb{E}f'(x)$ | low-variance gradients |
| Gumbel tricks | $\arg\max(z + g) \sim \mathrm{softmax}(z)$; relax with $\tau$ | discrete samples, relaxed |
| Bellman | $V^\pi = R_\pi + \gamma P_\pi V^\pi$; value iteration | evaluation and planning |
| Policy gradient theorem | $\sum_sd^\pi\sum_a\pi\nabla\log\pi\,Q^\pi$ | learning from episodes |
| KL regularization | $\pi^* \propto \pi_{\text{ref}}e^{\hat r/\beta}$ | safe optimization of a proxy |
