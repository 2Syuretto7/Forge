# Derivation: random variables, expectation and variance

## 1. Random variables and their distributions

A **random variable** is a function $X : \Omega \to \mathbb R$ that attaches a number to each outcome: the sum of two dice, the number of heads in ten flips, the time until a server fails. Its **distribution** says how probability spreads over the numbers.

- A **discrete** variable has a **probability mass function** (PMF) $p(k) = P(X = k)$, with $p(k) \ge 0$ and $\sum_k p(k) = 1$.
- A **continuous** variable has a **density** $f$, with $P(a \le X \le b) = \int_a^b f(x)\,dx$ and $\int f = 1$. A density is not a probability: $f$ can exceed 1, and every single point has probability 0.
- Both have a **cumulative distribution function** (CDF) $F(x) = P(X \le x)$, nondecreasing from 0 to 1.

For a density, $F(x) = \int_{-\infty}^x f(t)\,dt$, and the fundamental theorem of calculus gives $F' = f$.

:::edge{from=M17 text="the fundamental theorem: the density is the derivative of the CDF."}
:::

::::derivation{id=d1 title="Reading distributions"}
:::step
Let $X$ be the number of heads in 3 fair flips. Of the 8 equally likely sequences, 3 have two heads, so $P(X = 2) =$ [[3/8]].
:::
:::step
$F(1) = P(X \le 1) = \frac18 + \frac38 =$ [[1/2]].
:::
:::step
An exponential waiting time with rate $\lambda = 2$ has $F(x) = 1 - e^{-2x}$, so $P(X > 1) = e^{-2} \approx$ [[0.1353|tol=0.0005]].
:::
::::

## 2. Expectation

The **expectation** is the probability-weighted average, the balance point of the distribution:

$$
\mathbb{E}X = \sum_k k\,p(k) \qquad \text{or} \qquad \mathbb{E}X = \int x f(x)\,dx .
$$

To average a function of $X$, weight its values the same way: $\mathbb{E}[g(X)] = \sum_k g(k)\,p(k)$. **Linearity**

$$
\mathbb{E}[aX + bY + c] = a\,\mathbb{E}X + b\,\mathbb{E}Y + c
$$

holds always, independent or not, because a sum over outcomes splits term by term. With **indicators** ($1_A = 1$ if $A$ happens, else 0, so $\mathbb{E}1_A = P(A)$) it solves counting problems that look hard: write the count as a sum of indicators and add their probabilities.

But expectation passes only through sums and constants: in general $\mathbb{E}[g(X)] \ne g(\mathbb{E}X)$. The average of the squares is not the square of the average, and the difference is the subject of the next section.

::::derivation{id=d2 title="Expectations of a die and a shuffle"}
:::step
A fair die: $\mathbb{E}X = (1 + 2 + \dots + 6)/6 =$ [[3.5]].
:::
:::step
$\mathbb{E}X^2 = (1 + 4 + 9 + 16 + 25 + 36)/6 =$ [[91/6]].
:::
:::step
Shuffle 52 cards. Card $i$ stays in its place with probability $1/52$, so by linearity the expected number of cards that stay in place is [[1]], whatever the dependence between the cards.
:::
::::

## 3. Variance and covariance

The **variance** measures spread around the mean, and the **standard deviation** $\sigma = \sqrt{\operatorname{Var}X}$ puts it back in the units of $X$:

$$
\operatorname{Var}X = \mathbb{E}(X - \mu)^2 = \mathbb{E}X^2 - \mu^2, \qquad \operatorname{Var}(aX + b) = a^2 \operatorname{Var}X .
$$

Shifting does not change spread; scaling by $a$ scales $\sigma$ by $\lvert a\rvert$. The **covariance** of two variables measures how they move together:

$$
\operatorname{Cov}(X, Y) = \mathbb{E}[(X - \mu_X)(Y - \mu_Y)] = \mathbb{E}[XY] - \mu_X \mu_Y ,
$$

and expanding the square gives the rule for sums:

$$
\operatorname{Var}(X + Y) = \operatorname{Var}X + \operatorname{Var}Y + 2\operatorname{Cov}(X, Y) .
$$

If $X$ and $Y$ are independent, $\mathbb{E}[XY] = \mathbb{E}X\,\mathbb{E}Y$, the covariance is 0, and **variances add**. For $n$ independent copies of $X$, the sum has variance $n\sigma^2$, standard deviation $\sigma\sqrt n$, and the average $\bar X$ has variance $\sigma^2/n$.

**The geometry.** Centered random variables behave like vectors with the covariance as inner product: $\langle X, Y\rangle = \operatorname{Cov}(X, Y)$, squared length $\operatorname{Var}X$, and the **correlation** $\rho = \operatorname{Cov}(X, Y)/(\sigma_X\sigma_Y)$ is the cosine of the angle between them. Cauchy-Schwarz gives $-1 \le \rho \le 1$, the sum rule is the law of cosines, and uncorrelated variables are orthogonal: their variances add by Pythagoras.

:::edge{from=M12 text="covariance is an inner product, variance a squared length, and uncorrelated means orthogonal."}
:::

::::derivation{id=d3 title="Spreads"}
:::step
For a fair die, $\operatorname{Var}X = \frac{91}{6} - 3.5^2 =$ [[35/12]].
:::
:::step
$\operatorname{Var}(2X + 1) =$ [[35/3]].
:::
:::step
The puzzle: 512 independent terms of $\pm 0.01$, each with variance $10^{-4}$. The sum has standard deviation $\sqrt{0.0512} \approx$ [[0.2263|tol=0.001]].
:::
::::

::::predict{id=p3 kind=choice answer=c}
$X$ and $Y$ are independent, each with variance 1. What is $\operatorname{Var}(X - Y)$?

- 0
- 1
- 2
- 4

:::reveal
2. $\operatorname{Var}(X - Y) = \operatorname{Var}X + (-1)^2\operatorname{Var}Y - 2\operatorname{Cov}(X, Y) = 1 + 1 - 0$. Subtracting an independent variable adds its uncertainty; it cannot cancel it. Measuring a difference of two noisy quantities is noisier than either.
:::
::::

## 4. A family of distributions

| Name | PMF or density | Mean | Variance | Story |
| --- | --- | --- | --- | --- |
| Bernoulli($p$) | $P(1) = p$, $P(0) = 1 - p$ | $p$ | $p(1 - p)$ | one trial |
| Binomial($n, p$) | $\binom{n}{k} p^k (1 - p)^{n - k}$ | $np$ | $np(1 - p)$ | successes in $n$ trials |
| Poisson($\lambda$) | $e^{-\lambda}\lambda^k / k!$ | $\lambda$ | $\lambda$ | rare events in a fixed window |
| Uniform($a, b$) | $\frac{1}{b - a}$ on $[a, b]$ | $\frac{a + b}{2}$ | $\frac{(b - a)^2}{12}$ | no preference |
| Exponential($\lambda$) | $\lambda e^{-\lambda x}$, $x \ge 0$ | $\frac1\lambda$ | $\frac{1}{\lambda^2}$ | waiting time |
| Gaussian($\mu, \sigma^2$) | $\frac{1}{\sigma\sqrt{2\pi}} e^{-(x - \mu)^2/(2\sigma^2)}$ | $\mu$ | $\sigma^2$ | sums of many small effects |

The binomial is a sum of $n$ independent Bernoullis, so its mean and variance are $n$ times theirs. The Poisson is the binomial with many trials and a small chance each, $n \to \infty$ with $np = \lambda$ fixed; its gaps between events are exponential, and the exponential is **memoryless**: $P(X > s + t \mid X > s) = P(X > t)$.

Pick a distribution, draw a sample, and compare the sample mean and variance with the table. Small samples miss; large ones agree to a precision you will predict in M24.

:::widget{name=DistributionPlayground dist=poisson lam=3 n=200}
:::

::::derivation{id=d4 title="Exponential and Poisson"}
:::step
Integrating by parts, $\int_0^\infty x\,\lambda e^{-\lambda x}\,dx = \frac1\lambda$. A component that fails at rate $\lambda = 4$ per year lasts on average [[0.25]] years.
:::
:::step
Binomial($1000, 0.003$): $P(X = 0) = 0.997^{1000} \approx e^{-3} \approx$ [[0.0498|tol=0.0005]], the Poisson(3) value.
:::
::::

## 5. Sampling by the inverse CDF

Computers produce uniform numbers $U$ on $[0, 1)$. To turn them into samples with CDF $F$, invert it: $X = F^{-1}(U)$. Because $F$ is increasing,

$$
P(X \le x) = P(F^{-1}(U) \le x) = P(U \le F(x)) = F(x) .
$$

For the exponential, $u = 1 - e^{-\lambda x}$ gives $x = -\log(1 - u)/\lambda$; at $u = \frac12$ that is the median, $\log 2/\lambda$. For a discrete variable, split $[0, 1)$ into pieces of lengths $p(0), p(1), \dots$ and return the piece $U$ lands in: a search in the cumulative sums. The Gaussian CDF has no closed-form inverse; the **Box-Muller** transform maps two uniforms to two independent Gaussians through polar coordinates, the M20 change of variables run backwards.

The derivative of $F(F^{-1}(u)) = u$ gives $(F^{-1})'(u) = 1/f(F^{-1}(u))$: where the density is thin, the quantile is steep, and evenly spread uniforms are stretched apart.

## 6. Variance and initialization

A neuron computes $y = \sum_{i=1}^n w_i x_i$. Initialize the weights independently with mean 0 and variance $s^2$, independent of inputs with $\mathbb{E}x_i^2 = q$. Each term has mean 0 and variance $\mathbb{E}w_i^2\,\mathbb{E}x_i^2 = s^2 q$, and the terms are uncorrelated, so

$$
\operatorname{Var}y = n s^2 q .
$$

To pass the second moment through unchanged, choose $s^2 = 1/n$: the weight scale shrinks like $1/\sqrt n$. A ReLU after the layer zeroes the negative half of a symmetric $y$ and keeps $\mathbb{E}\max(y, 0)^2 = \frac12\operatorname{Var}y$, so ReLU networks need $s^2 = 2/n$. Through $L$ layers the second moment is multiplied by the per-layer factor $L$ times: any factor other than 1 grows or decays exponentially with depth.

::::derivation{id=d5 title="The initialization scale"}
:::step
512 inputs with $q = 1$, no activation: the variance-preserving weight variance is $s^2 =$ [[1/512]].
:::
:::step
With a ReLU after each layer: $s = \sqrt{2/512} =$ [[0.0625]].
:::
:::step
Weights 10 percent too large in a linear network multiply the second moment by $1.1^2 = 1.21$ per layer; after 50 layers it has grown by $1.21^{50} \approx$ [[13780|tol=200]].
:::
::::

:::edge{to=M23 text="joint distributions, covariance matrices and the multivariate Gaussian."}
:::

:::edge{to=M24 text="the average's variance sigma^2/n becomes the law of large numbers and the central limit theorem."}
:::

:::edge{to=M27 text="entropy, the expectation of minus the log probability."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Random variable | a number for each outcome | losses, weights, counts |
| PMF, density, CDF | $p(k)$, $f$ with $F' = f$, $F(x) = P(X \le x)$ | describe a distribution |
| Linearity | $\mathbb{E}[aX + bY] = a\mathbb{E}X + b\mathbb{E}Y$, always | indicators, sums |
| Variance | $\mathbb{E}X^2 - \mu^2$, scales by $a^2$ | spread |
| Sum rule | $\operatorname{Var}(X + Y) = \operatorname{Var}X + \operatorname{Var}Y + 2\operatorname{Cov}$ | independent variances add |
| Families | Bernoulli, binomial, Poisson, uniform, exponential, Gaussian | models of noise and counts |
| Inverse CDF | $F^{-1}(U)$ has CDF $F$ | sampling |
| Initialization | $\operatorname{Var}y = n s^2 q$, so $s^2 = 1/n$ or $2/n$ | stable deep networks |
