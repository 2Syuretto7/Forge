# Derivation: from random variables to the bootstrap

This movement builds one chain of ideas: random variables and their averages, the distributions we will use all course, Bayes' rule, the likelihood and its maximizer, priors and the MAP estimate, the bias of estimators, and the two limit theorems that make estimates trustworthy. It ends with the bootstrap, the tool you will use whenever a formula for uncertainty is out of reach.

## 1. Random variables

A **random variable** $X$ is a number produced by a random process. A discrete one has a **probability mass function** $p(x) = P(X = x)$ with $\sum_x p(x) = 1$. A continuous one has a **density** $p(x)$ with $\int p(x)\,dx = 1$; probabilities are areas, $P(a \le X \le b) = \int_a^b p(x)\,dx$, and the density itself can exceed 1.

The **expectation** is the probability-weighted average,

$$
\mathbb{E}[X] = \sum_x x\, p(x) \quad\text{or}\quad \int x\, p(x)\,dx ,
$$

and the **variance** measures spread around it: $\operatorname{Var}(X) = \mathbb{E}\big[(X - \mathbb{E}X)^2\big] = \mathbb{E}[X^2] - (\mathbb{E}X)^2$.

Two rules do most of the work. Expectation is **linear**: $\mathbb{E}[aX + bY] = a\,\mathbb{E}X + b\,\mathbb{E}Y$ for any random variables, independent or not. Variance scales quadratically, $\operatorname{Var}(aX + b) = a^2 \operatorname{Var}(X)$, and adds for **independent** variables: $\operatorname{Var}(X + Y) = \operatorname{Var}X + \operatorname{Var}Y$.

::::derivation{id=d1 title="Moments of a coin and of an average"}
:::step
A Bernoulli variable takes the value 1 with probability $p$ and 0 otherwise. Its mean is $\mathbb{E}X = 1 \cdot p + 0 \cdot (1-p) =$ [[p]].
:::
:::step
Since $X^2 = X$ for a 0/1 variable, $\mathbb{E}[X^2] = p$, and the variance is $p - p^2 =$ [[p*(1-p)]].
:::
:::step
Let $\bar X = \frac{1}{n}\sum_{i=1}^n X_i$ for independent copies with variance $\sigma^2$. By the scaling and addition rules, $\operatorname{Var}(\bar X) = \frac{1}{n^2} \cdot n\sigma^2 =$ [[sigma^2/n]].
:::
:::step
So the **standard error** of a mean, its typical distance from the truth, is $\sigma/\sqrt{n}$. Halving the error needs [[4]] times as much data.
:::
::::

## 2. The distributions we will use

**Bernoulli and binomial.** A single coin flip is Bernoulli($p$). The number of heads $K$ in $n$ independent flips is binomial: $P(K = k) = \binom{n}{k} p^k (1-p)^{n-k}$, with mean $np$ and variance $np(1-p)$.

**Categorical.** A die with $K$ faces and probabilities $\pi_1, \dots, \pi_K$ summing to one. Next-token prediction in a language model is a categorical distribution over the vocabulary; it is the object of L04 and L14.

**Gaussian.** The normal density with mean $\mu$ and variance $\sigma^2$ is

$$
\mathcal{N}(x;\, \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\Big(-\frac{(x-\mu)^2}{2\sigma^2}\Big).
$$

It is the limit shape of averages (Section 7), the maximum-entropy distribution for a given variance (L04), and the noise model that turns least squares into maximum likelihood (L05). If $Z \sim \mathcal{N}(0, 1)$ then $\mu + \sigma Z \sim \mathcal{N}(\mu, \sigma^2)$, which is how you sample from any Gaussian given a standard one.

**Sampling from a uniform.** Every distribution can be sampled from uniform random numbers $U \sim \text{Uniform}(0,1)$. For a discrete distribution, split $[0,1)$ into intervals of lengths $\pi_1, \pi_2, \dots$ and return the interval $U$ lands in. For a continuous one with cumulative distribution function $F$, return $F^{-1}(U)$ (the **inverse-CDF** method): $P(F^{-1}(U) \le x) = P(U \le F(x)) = F(x)$.

::::derivation{id=d2 title="Inverse-CDF sampling for the exponential"}
:::step
The exponential distribution with rate $\lambda$ has $F(x) = 1 - e^{-\lambda x}$ for $x \ge 0$. Solving $u = 1 - e^{-\lambda x}$ for $x$ gives $x = F^{-1}(u) =$ [[-log(1-u)/lambda]].
:::
:::step
Its mean is $1/\lambda$. With $\lambda = 2$, a large sample produced this way should average about [[0.5]].
:::
::::

## 3. Bayes' rule

Conditional probability is $P(A \mid B) = P(A, B) / P(B)$. Writing the joint probability both ways, $P(A, B) = P(A \mid B) P(B) = P(B \mid A) P(A)$, gives **Bayes' rule**:

$$
P(H \mid D) = \frac{P(D \mid H)\, P(H)}{P(D)}, \qquad P(D) = \sum_{H'} P(D \mid H')\, P(H').
$$

Read it as: posterior equals likelihood times prior, renormalized. The denominator only makes the posterior sum to one.

::::derivation{id=d3 title="A positive test for a rare condition"}
:::step
A condition affects $1\%$ of people. A test detects it $99\%$ of the time and gives a false positive $5\%$ of the time. The probability of a positive result for a person who has the condition, times the prior, is $0.99 \times 0.01 =$ [[0.0099]].
:::
:::step
The total probability of a positive result is $0.0099 + 0.05 \times 0.99 =$ [[0.0594]].
:::
:::step
So $P(\text{condition} \mid \text{positive}) = 0.0099 / 0.0594 \approx$ [[0.1667]]. Five out of six positives are false, because healthy people vastly outnumber sick ones.
:::
::::

## 4. The likelihood and maximum likelihood

Fix a model $p(x \mid \theta)$ and observe independent data $x_1, \dots, x_n$. The **likelihood** is the probability of the data as a function of the parameter,

$$
L(\theta) = \prod_{i=1}^n p(x_i \mid \theta), \qquad \ell(\theta) = \log L(\theta) = \sum_{i=1}^n \log p(x_i \mid \theta).
$$

It is not a distribution over $\theta$: it need not integrate to one. The **maximum likelihood estimate** (MLE) is the parameter that makes the data most probable, $\hat\theta = \arg\max_\theta \ell(\theta)$. We maximize the log because sums are easier to differentiate than products, and because a product of thousands of probabilities underflows to zero in floating point.

::::derivation{id=d4 title="The MLE of a coin"}
:::step
With $k$ heads in $n$ flips, $\ell(p) = k \log p + (n - k)\log(1-p)$. Its derivative is $\ell'(p) = k/p -$ [[(n-k)/(1-p)]].
:::
:::step
Setting $\ell'(p) = 0$ and solving gives $\hat p =$ [[k/n]]: the observed frequency.
:::
:::step
The second derivative, $-k/p^2 - (n-k)/(1-p)^2$, is negative, so this is a maximum. At $\hat p$ it equals $-n/(\hat p(1-\hat p))$. Its negative reciprocal, $\hat p(1 - \hat p)/n$, is the squared standard error of $\hat p$. For $\hat p = 0.5$ and $n = 100$ the standard error is [[0.05]].
:::
::::

The curvature of the log-likelihood at its peak measures how sharply the data pin down the parameter. A flat peak (few flips) means a wide range of parameters explain the data almost equally well. The widget shows both the fit and the curve.

:::widget{name=DistributionPlayground dist=gaussian mu=1 sigma=1.5 n=10}
:::

::::derivation{id=d5 title="The MLE of a Gaussian"}
:::step
For data $x_i$ and model $\mathcal{N}(\mu, \sigma^2)$, $\ell(\mu, \sigma) = -\frac{n}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_i (x_i - \mu)^2$. For a single data point $x$, the derivative of the second term with respect to $\mu$ is [[(x-mu)/sigma^2]].
:::
:::step
Summing over points and setting the derivative to zero gives $\sum_i (x_i - \mu) = 0$, so $\hat\mu = \bar x$, the sample mean.
:::
:::step
Differentiating with respect to $\sigma$ gives $-n/\sigma + \frac{1}{\sigma^3}\sum_i (x_i - \hat\mu)^2 = 0$, so $\hat\sigma^2 = \frac{1}{n}\sum_i (x_i - \bar x)^2$. With $n = 4$ and squared deviations summing to $12$, $\hat\sigma^2 =$ [[3]].
:::
::::

:::edge{to=L04 text="Maximizing average log-likelihood is minimizing cross-entropy between the data and the model."}
:::

:::edge{to=L05 text="Gaussian noise turns the MLE of a linear model into least squares; Bernoulli noise turns it into logistic regression."}
:::

## 5. Priors, posteriors and the MAP estimate

The MLE uses only the data. With little data it can be extreme: three tails in three flips gives $\hat p = 0$, a claim that heads is impossible. Bayes' rule lets you combine the data with a prior $p(\theta)$:

$$
p(\theta \mid x_{1:n}) \propto p(x_{1:n} \mid \theta)\; p(\theta).
$$

The **maximum a posteriori** (MAP) estimate maximizes the posterior, $\arg\max_\theta \big[\ell(\theta) + \log p(\theta)\big]$: the log-prior acts as a penalty added to the log-likelihood.

For a coin, the **Beta** prior $p(\theta) \propto \theta^{a-1}(1-\theta)^{b-1}$ is convenient because multiplying it by the likelihood $\theta^k (1-\theta)^{n-k}$ gives another Beta: the posterior is $\text{Beta}(a + k,\; b + n - k)$. The prior behaves like $a$ imaginary heads and $b$ imaginary tails added to the data. A prior with this property is called **conjugate**.

::::derivation{id=d6 title="MAP and posterior mean for a coin"}
:::step
The posterior density is proportional to $\theta^{a+k-1}(1-\theta)^{b+n-k-1}$. Maximizing its logarithm as in the MLE derivation gives $\theta_{\text{MAP}} = \dfrac{a + k - 1}{a + b + n - 2}$. With a uniform prior ($a = b = 1$) the MAP equals the MLE, which is [[k/n]].
:::
:::step
The posterior mean of a $\text{Beta}(\alpha, \beta)$ is $\alpha/(\alpha + \beta)$, so here it is $(a+k)/(a+b+n)$. With $a = b = 1$ and three tails in three flips, the posterior mean is [[1/5]] instead of $0$.
:::
:::step
Adding one imaginary head and one imaginary tail is known as **Laplace smoothing**. For coin A of the puzzle (3 heads in 4 flips) the uniform-prior posterior is $\text{Beta}(4, 2)$, with mean [[2/3]].
:::
::::

A Gaussian prior $\theta \sim \mathcal{N}(0, \tau^2)$ contributes $-\theta^2/(2\tau^2)$ to the log posterior: an L2 penalty. That is the origin of weight decay, derived properly in L05.

## 6. Estimators and their bias

An **estimator** is any rule that turns data into a guess $\hat\theta$. Because the data are random, $\hat\theta$ is random too, and we judge it by its distribution. Its **bias** is $\mathbb{E}[\hat\theta] - \theta$, and its mean squared error splits as

$$
\mathbb{E}\big[(\hat\theta - \theta)^2\big] = \text{bias}^2 + \operatorname{Var}(\hat\theta).
$$

The Gaussian MLE of the variance is biased. The deviations $x_i - \bar x$ are measured from a mean fitted to the same points, which sits closer to them than the true mean does.

::::derivation{id=d7 title="Why the variance MLE divides by the wrong n"}
:::step
Write $x_i - \bar x = (x_i - \mu) - (\bar x - \mu)$. Expanding and summing, $\sum_i (x_i - \bar x)^2 = \sum_i (x_i - \mu)^2 - n(\bar x - \mu)^2$. The expectation of the first sum is $n\sigma^2$. The expectation of $n(\bar x - \mu)^2$ is $n \operatorname{Var}(\bar x) =$ [[sigma^2]].
:::
:::step
So $\mathbb{E}\big[\sum_i (x_i - \bar x)^2\big] = (n - 1)\sigma^2$, and the MLE $\hat\sigma^2 = \frac{1}{n}\sum_i (x_i - \bar x)^2$ has expectation [[(n-1)/n*sigma^2]].
:::
:::step
Its bias is therefore $-\sigma^2/n$. Dividing by $n - 1$ instead removes it. With $n = 5$ and $\sigma^2 = 10$, the MLE is too small on average by [[2]].
:::
::::

Unbiasedness is not everything: the biased MLE actually has lower mean squared error than the unbiased version for Gaussian data. L06 develops this tradeoff for prediction error.

## 7. Why averages work: the law of large numbers and the CLT

**Law of large numbers.** Since $\operatorname{Var}(\bar X) = \sigma^2/n \to 0$, the sample mean concentrates around $\mu$. Chebyshev's inequality makes it quantitative: $P(|\bar X - \mu| \ge \epsilon) \le \sigma^2/(n\epsilon^2)$.

**Central limit theorem.** If the $X_i$ are independent with mean $\mu$ and finite variance $\sigma^2$, then the standardized mean

$$
Z_n = \frac{\bar X - \mu}{\sigma/\sqrt{n}}
$$

has a distribution that approaches $\mathcal{N}(0,1)$ as $n$ grows, whatever the shape of the distribution of each $X_i$. Averages of skewed, discrete or bounded variables all end up looking Gaussian. That is why $\bar x \pm 1.96\,\sigma/\sqrt{n}$ is an approximate 95 percent confidence interval: a standard normal lies within $\pm 1.96$ with probability $0.95$.

The condition "finite variance" is not decoration. For the Cauchy distribution the mean of $n$ draws has exactly the same distribution as a single draw: averaging does nothing. Movement 5 breaks the sample mean this way.

You will check the CLT by simulation in the build movement rather than prove it; the standard proof uses characteristic functions and is beyond what we need.

## 8. The bootstrap

Formulas like $\sigma/\sqrt{n}$ exist for means. For a median, a ratio of two means, an accuracy difference between two models, or the area under a curve, they are hard or unavailable. The **bootstrap** replaces the formula with computation.

The idea is the **plug-in principle**: you do not know the true distribution $F$, but the data define an empirical distribution $\hat F$ that puts mass $1/n$ on each observation. Sampling $n$ points from $\hat F$ is sampling with replacement from the data. So:

1. Draw $B$ resamples of size $n$ with replacement.
2. Compute the statistic on each resample: $\hat\theta^{*1}, \dots, \hat\theta^{*B}$.
3. The spread of the $\hat\theta^{*b}$ estimates the spread of $\hat\theta$. The **percentile interval** takes their 2.5th and 97.5th percentiles.

::::derivation{id=d8 title="How often an observation is left out"}
:::step
A resample draws $n$ times with replacement. The probability that a given observation is never drawn is $(1 - 1/n)^n$. For large $n$ this approaches $e^{-1} \approx$ [[0.368]].
:::
:::step
So each resample contains about $1 - 0.368 = 63\%$ of the distinct observations. For $n = 2$, the exact probability of leaving out a given point is $(1/2)^2 =$ [[0.25]].
:::
::::

The bootstrap needs the observations to be independent and the sample to be representative; it inherits every flaw of the data. With tiny samples or extreme statistics (the maximum, rare events) it can be badly wrong, a failure you will provoke in the capstone.

:::edge{to=L23 text="Benchmark scores are means over items; L23 puts bootstrap confidence intervals on them and on model differences."}
:::

:::edge{to=L06 text="Bias and variance of estimators become the bias-variance decomposition of a model's test error."}
:::

## Back to the two coins

With uniform priors, coin A has posterior $\text{Beta}(4, 2)$ and coin B $\text{Beta}(7, 5)$. The probability that A has the larger bias is $P(\theta_A > \theta_B) = \int_0^1 p_A(t)\, F_B(t)\, dt$, where $F_B$ is B's posterior CDF. Numerically it is about $0.65$. You will compute it two ways in Movement 4: by integration on a grid and by Monte Carlo sampling from the two posteriors.

## Summary

| Idea | Formula | Where it comes back |
| --- | --- | --- |
| Standard error | $\sigma/\sqrt{n}$ | every confidence interval |
| Bayes' rule | posterior $\propto$ likelihood $\times$ prior | RLHF reward models (L21) |
| MLE | $\arg\max_\theta \sum_i \log p(x_i \mid \theta)$ | every training loss (L04, L05, L14) |
| MAP | MLE plus log-prior | weight decay (L05, L09) |
| Variance bias | $\mathbb{E}\hat\sigma^2 = \frac{n-1}{n}\sigma^2$ | batch statistics in normalization (L10) |
| CLT | $(\bar X - \mu)/(\sigma/\sqrt n) \to \mathcal{N}(0,1)$ | eval error bars (L23) |
| Bootstrap | resample, recompute, take percentiles | eval confidence intervals (L23) |
