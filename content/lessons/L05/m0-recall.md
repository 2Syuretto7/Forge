# Recall bridge: projections and likelihoods

This lesson joins two threads. From L01 it takes least squares and the normal equations; from L02 the likelihood, maximum likelihood and priors. Reviews due from those lessons appear above.

## From L01

The least-squares solution $\hat w = \arg\min_w \|Xw - y\|^2$ satisfies $X^\top X \hat w = X^\top y$, and the fit $X\hat w$ is the projection of $y$ onto the column space of $X$. Solving through QR is more accurate than forming $X^\top X$.

## From L02

The MLE maximizes $\sum_i \log p(y_i \mid \theta)$; a prior adds $\log p(\theta)$ and gives the MAP estimate; a Gaussian prior contributes $-\|\theta\|^2/(2\tau^2)$.

::::derivation{id=d0 title="Warm-up"}
:::step
The Gaussian log-density $\log \mathcal N(y; m, \sigma^2) = -\tfrac12\log(2\pi\sigma^2) - \dfrac{(y-m)^2}{2\sigma^2}$. Its derivative with respect to $m$ is [[(y-m)/sigma^2]].
:::
:::step
The Bernoulli log-likelihood of label $y \in \{0,1\}$ with $P(y=1) = s$ is $y\log s + (1-y)\log(1-s)$. At $y = 1$ and $s = 0.8$ it equals $\ln 0.8 \approx$ [[-0.2231]].
:::
:::step
With $s = \sigma(a)$, the derivative of $\log\sigma(a)$ is $1 - \sigma(a)$. At $a = 0$ it is [[0.5]].
:::
::::
