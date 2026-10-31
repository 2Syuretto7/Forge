# Derivation: likelihood, MLE, MAP and the bootstrap

## 1. Estimators, bias and variance

An **estimator** is a rule that turns data into a guess $\hat\theta$ of a parameter $\theta$. The data are random, so $\hat\theta$ is a random variable with a **sampling distribution**, and you judge the rule by it: its **bias** $\mathbb{E}\hat\theta - \theta$ and its variance. They combine in the mean squared error of the estimator:

$$
\mathbb{E}\big[(\hat\theta - \theta)^2\big] = \text{bias}^2 + \operatorname{Var}\hat\theta ,
$$

the M22 decomposition $\mathbb{E}(X - c)^2 = \operatorname{Var}X + (\mathbb{E}X - c)^2$ with $X = \hat\theta$ and $c = \theta$.

The variance of a sample is the classic biased estimator. Deviations from the sample mean are smaller than deviations from the true mean, because $\bar x$ was fitted to the same points: $\sum_i (x_i - \bar x)^2 = \sum_i (x_i - \mu)^2 - n(\bar x - \mu)^2$, whose expectation is $n\sigma^2 - \sigma^2$.

::::derivation{id=d1 title="Dividing by n - 1"}
:::step
With $n = 5$ and $\sigma^2 = 4$, the average of $\frac1n\sum_i (x_i - \bar x)^2$ over many samples is $\frac{n - 1}{n}\sigma^2 =$ [[3.2]].
:::
:::step
Multiplying by [[5/4]] removes the bias: that is division by $n - 1$.
:::
::::

Unbiased is not the same as best: the biased version has the smaller mean squared error for Gaussian data, and later sections deliberately add bias (priors, shrinkage) to cut variance.

## 2. The likelihood and maximum likelihood

Fix a model $p(x \mid \theta)$ and independent data $x_1, \dots, x_n$. The **likelihood** is the probability of the data as a function of the parameter, and its logarithm turns the product into a sum:

$$
L(\theta) = \prod_{i=1}^n p(x_i \mid \theta), \qquad \ell(\theta) = \sum_{i=1}^n \log p(x_i \mid \theta) .
$$

The **maximum likelihood estimate** (MLE) is $\hat\theta = \arg\max_\theta \ell(\theta)$: the parameter under which the observed data were most probable. Logarithms also keep the computation finite: a product of ten thousand probabilities underflows to 0 in floating point.

::::predict{id=p3 kind=choice answer=b}
For 7 heads in 10 flips, $L(p) = \binom{10}{7}p^7(1 - p)^3$. Integrate it over $p$ from 0 to 1. What do you get?

- 1, as for any probability distribution.
- $1/11$.
- $0.7$.
- It diverges.

:::reveal
$1/11$: the Beta integral $\int_0^1 p^7(1 - p)^3\,dp = \frac{7!\,3!}{11!}$ times $\binom{10}{7}$. The likelihood is a probability of the data for each $p$, not a probability distribution over $p$. To get one you need a prior and Bayes' rule, Section 5.
:::
::::

::::derivation{id=d2 title="The MLE of a coin"}
:::step
For 7 heads in 10, $\ell(p) = 7\log p + 3\log(1 - p)$, and $\ell'(p) = 7/p - 3/(1 - p) = 0$ at $\hat p =$ [[0.7]].
:::
:::step
The curvature there is $\ell''(\hat p) = -n/(\hat p(1 - \hat p)) \approx -47.6$, and the standard error $1/\sqrt{47.6} \approx$ [[0.145|tol=0.002]].
:::
::::

For a Gaussian, $\hat\mu = \bar x$ and $\hat\sigma^2 = \frac1n\sum_i (x_i - \bar x)^2$, the biased estimator of Section 1. For a categorical distribution with probabilities written as a softmax of logits, the gradient of the negative log-likelihood is $N\pi - c$, predicted counts minus observed counts: the gradient of every classifier you will train. The MLE is **invariant**: the MLE of $g(\theta)$ is $g(\hat\theta)$, so the MLE of an exponential rate is $1/\bar x$, and invariance does not preserve unbiasedness.

## 3. Fisher information and standard errors

Near its peak the log-likelihood is a parabola (M16's Taylor expansion), and its curvature says how sharply the data pin down $\theta$. The **Fisher information** is the expected curvature,

$$
I(\theta) = \mathbb{E}\big[-\ell''(\theta)\big] ,
$$

which grows in proportion to $n$. For large $n$ the MLE is approximately $N(\theta, 1/I(\theta))$, so $1/\sqrt{I(\hat\theta)}$ is its standard error. For the Poisson, $\ell''(\lambda) = -\sum_i x_i/\lambda^2$ and $I(\lambda) = n/\lambda$; for the coin, $I(p) = n/(p(1 - p))$. No unbiased estimator can have variance below $1/I(\theta)$ (the Cramer-Rao bound), and the MLE reaches it as $n$ grows.

## 4. Least squares is maximum likelihood

Model $y_i = w^\top x_i + \varepsilon_i$ with independent $\varepsilon_i \sim N(0, \sigma^2)$. Then

$$
-\ell(w, \sigma) = \frac n2\log(2\pi\sigma^2) + \frac{1}{2\sigma^2}\sum_i (y_i - w^\top x_i)^2 .
$$

For every $\sigma$, the best $w$ minimizes the sum of squared residuals: **the MLE of $w$ is the least-squares solution** of M12. Setting the derivative in $\sigma^2$ to zero gives $\hat\sigma^2 = \text{RSS}/n$. Other noise models give other losses: Laplace noise gives absolute errors, Bernoulli labels give logistic regression.

:::edge{from=M12 text="least squares is maximum likelihood under Gaussian noise."}
:::

::::derivation{id=d3 title="The noise variance"}
:::step
A line fitted to 4 points leaves a residual sum of squares of 12. The MLE of the noise variance is [[3]].
:::
::::

## 5. Bayesian inference and conjugate priors

The Bayesian treats $\theta$ as uncertain and describes that uncertainty by a **prior** $p(\theta)$. Bayes' rule (M21) gives the **posterior**:

$$
p(\theta \mid x_{1:n}) = \frac{p(x_{1:n} \mid \theta)\,p(\theta)}{p(x_{1:n})} \propto L(\theta)\,p(\theta) .
$$

The likelihood carries the data, the prior everything else, and the posterior is a full distribution over $\theta$: its mean, its mode and its intervals are all available. For a coin, the **Beta** prior $p(\theta) \propto \theta^{a - 1}(1 - \theta)^{b - 1}$ times the likelihood $\theta^k(1 - \theta)^{n - k}$ is again a Beta, $\text{Beta}(a + k, b + n - k)$: the prior acts as $a$ imaginary heads and $b$ imaginary tails. A prior that stays in its family under updating is **conjugate**. As $n$ grows the data overwhelm any reasonable prior, and the posterior concentrates around the MLE with spread $1/\sqrt{I}$.

::::derivation{id=d4 title="Seven heads, Bayesian"}
:::step
Uniform prior, 7 heads and 3 tails: the posterior is Beta(8, 4), with mean [[2/3]].
:::
:::step
Its mode, the most probable value, is $(8 - 1)/(8 + 4 - 2) =$ [[0.7]], equal to the MLE.
:::
::::

## 6. MAP: a Gaussian prior is a penalty

The **maximum a posteriori** (MAP) estimate maximizes the posterior, which in logarithms is

$$
\hat\theta_{\text{MAP}} = \arg\max_\theta \big[\ell(\theta) + \log p(\theta)\big] :
$$

the MLE plus a penalty from the prior. A Gaussian prior on regression weights, $w \sim N(0, \tau^2 I)$, contributes $-\lVert w\rVert^2/(2\tau^2)$, so with noise variance $\sigma^2$ the MAP minimizes

$$
\frac{1}{2\sigma^2}\lVert y - Xw\rVert^2 + \frac{1}{2\tau^2}\lVert w\rVert^2 ,
$$

**ridge regression** with $\lambda = \sigma^2/\tau^2$. A narrow prior is a strong penalty. Weight decay in neural networks is this penalty; a Laplace prior gives the L1 penalty of the lasso.

::::derivation{id=d5 title="The ridge penalty"}
:::step
Noise standard deviation $\sigma = 1$ and prior standard deviation $\tau = 0.5$ give the ridge penalty $\lambda = \sigma^2/\tau^2 =$ [[4]].
:::
::::

## 7. The bootstrap

Formulas like $s/\sqrt n$ and $1/\sqrt{I}$ exist for simple estimators. For a median, a ratio, the difference in accuracy between two models or an area under a curve, the **bootstrap** replaces the formula by computation. Its **plug-in principle**: the true distribution is unknown, but the data define an empirical distribution with mass $1/n$ on each point, and sampling $n$ points from it is resampling the data with replacement.

1. Draw $B$ resamples of size $n$ with replacement.
2. Compute the statistic on each: $\hat\theta^{*1}, \dots, \hat\theta^{*B}$.
3. Their spread estimates the spread of $\hat\theta$; the **percentile interval** takes their 2.5th and 97.5th percentiles.

Each resample leaves out about $e^{-1} \approx 37$ percent of the points. The bootstrap inherits every assumption of resampling single points: independence, and a sample large enough to stand in for the population. Small samples, statistics that depend on extremes, and dependent data break it, as Movement 5 shows.

:::edge{to=L23 text="Benchmark scores are means over items; the bootstrap puts intervals on them and on model differences."}
:::

## 8. Confidence and credible intervals

A 95 percent **confidence interval** is a procedure: over repeated samples, it contains the fixed true $\theta$ 95 percent of the time. Any single interval either contains it or not. A 95 percent **credible interval** is a statement about one posterior: given these data and this prior, $\theta$ lies in it with probability $0.95$. They answer different questions, and with much data and a mild prior they nearly coincide. With little data they can differ, and the textbook Wald interval $\hat p \pm 1.96\sqrt{\hat p(1 - \hat p)/n}$ can fail badly: after 0 successes in 20 trials it is the single point 0. Asking how often an interval covers, as M24's capstone did, is the way to judge any of them.

:::edge{to=L05 text="ridge regression and logistic regression, as MAP and MLE."}
:::

:::edge{to=M27 text="maximizing likelihood is minimizing cross-entropy."}
:::

:::edge{to=M28 text="negative log-likelihoods of exponential families are convex."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Mean squared error | $\text{bias}^2 + \text{variance}$ | judge estimators |
| Likelihood | $\ell(\theta) = \sum_i \log p(x_i \mid \theta)$, not a distribution over $\theta$ | fit models |
| MLE | $\arg\max \ell$; coin $k/n$, Gaussian $\bar x$ and $\frac1n\sum (x_i - \bar x)^2$ | default estimator |
| Fisher information | $I = \mathbb{E}[-\ell'']$, SE $\approx 1/\sqrt{I}$ | error bars from curvature |
| Least squares | MLE under Gaussian noise, $\hat\sigma^2 = \text{RSS}/n$ | regression |
| Posterior | $\propto$ likelihood $\times$ prior; Beta-Binomial conjugate | uncertainty over $\theta$ |
| MAP | MLE plus log-prior; Gaussian prior gives ridge | regularization |
| Bootstrap | resample, recompute, take percentiles | error bars without formulas |
