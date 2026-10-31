# Derivation: limit theorems and Monte Carlo

## 1. Markov and Chebyshev

**Markov's inequality.** For a nonnegative random variable and $a > 0$,

$$
P(X \ge a) \le \frac{\mathbb{E}X}{a} .
$$

Proof: $X \ge a\,1_{X \ge a}$ everywhere, because where $X \ge a$ the right side is $a$ and elsewhere it is 0; take expectations. **Chebyshev's inequality** applies Markov to the nonnegative variable $(X - \mu)^2$ at $a = \varepsilon^2$:

$$
P(\lvert X - \mu\rvert \ge \varepsilon) \le \frac{\sigma^2}{\varepsilon^2} .
$$

Both use almost nothing about the distribution, so both are loose for most distributions; but each is attained by some distribution, so neither can be improved without more information.

::::derivation{id=d1 title="Bounds from a mean and a variance"}
:::step
A server's average response time is 200 ms. Markov bounds the fraction of responses taking at least 1 second by $200/1000 =$ [[0.2]].
:::
:::step
Chebyshev: a variable is at least 3 standard deviations from its mean with probability at most [[1/9]].
:::
::::

## 2. The law of large numbers

Let $\bar X_n$ be the average of $n$ independent copies of $X$, with mean $\mu$ and variance $\sigma^2$. Then $\operatorname{Var}\bar X_n = \sigma^2/n$, and Chebyshev gives

$$
P(\lvert \bar X_n - \mu\rvert \ge \varepsilon) \le \frac{\sigma^2}{n\varepsilon^2} \to 0 \qquad \text{for every } \varepsilon > 0 .
$$

This is the **weak law of large numbers**: the average converges to the mean in probability. It is a limit in M15's sense, applied to probabilities instead of numbers.

:::edge{from=M15 text="the law of large numbers is an epsilon statement about a limit."}
:::

::::derivation{id=d2 title="How many flips?"}
:::step
A fair coin has $\sigma^2 = \frac14$. Chebyshev guarantees that the frequency of heads is within $0.01$ of $\frac12$ with probability at least 95 percent once $n \ge \frac{1/4}{0.01^2 \times 0.05} =$ [[50000]].
:::
::::

::::predict{id=p3 kind=choice answer=a}
Chebyshev bounds the probability that a standard normal variable lands at least 2 from its mean by $\frac14$. What is the true probability?

- About 0.046
- About 0.25
- About 0.16
- About 0.005

:::reveal
About $0.046$. Chebyshev must hold for every distribution with that variance, including the three-point one that attains it, so for any particular distribution it is pessimistic. For the coin above, the central limit theorem says about 9,600 flips suffice, not 50,000.
:::
::::

## 3. The central limit theorem

Standardize the sum: $Z_n = \frac{\bar X_n - \mu}{\sigma/\sqrt n}$. The **central limit theorem**: if $\sigma^2$ is finite, then for every $z$,

$$
P(Z_n \le z) \to \Phi(z), \qquad \text{the standard normal CDF} .
$$

**A sketch through moment generating functions.** The MGF $M(t) = \mathbb{E}e^{tX}$ holds every moment: $M'(0) = \mathbb{E}X$, $M''(0) = \mathbb{E}X^2$. For a sum of independent variables, the exponentials multiply, so MGFs multiply. Take $\mu = 0$, $\sigma = 1$; then $Z_n = \frac{1}{\sqrt n}\sum X_i$ has

$$
\mathbb{E}e^{tZ_n} = M\big(t/\sqrt n\big)^n = \Big(1 + \frac{t^2}{2n} + o\big(\tfrac1n\big)\Big)^n \to e^{t^2/2} ,
$$

by Taylor's theorem at 0 and M06's limit $(1 + x/n)^n \to e^x$. And $e^{t^2/2}$ is the MGF of the standard normal. Every distribution with finite variance loses all but its first two moments in the limit; skewness fades like $1/\sqrt n$, which is why skewed distributions need more terms.

In practice: $\bar X_n$ is approximately $N(\mu, \sigma^2/n)$, and $\bar x \pm 1.96\,s/\sqrt n$ is an approximate **95 percent confidence interval**.

::::derivation{id=d3 title="Thirty dice"}
:::step
The average of 30 rolls has standard deviation $\sqrt{35/12}/\sqrt{30} \approx$ [[0.312|tol=0.002]].
:::
:::step
An average above 4 is $0.5/0.312 \approx 1.60$ standard deviations above the mean, which has probability about [[0.054|tol=0.003]].
:::
::::

## 4. Monte Carlo integration

Any integral can be written as an expectation: $\int_a^b f(x)\,dx = (b - a)\,\mathbb{E}f(U)$ for $U$ uniform on $[a, b]$, and in many dimensions likewise over any region you can sample. The **Monte Carlo estimate** averages $(b - a)f(U_i)$; it is unbiased, and by Section 3 its **standard error** is

$$
\text{SE} = \frac{s}{\sqrt n} ,
$$

where $s$ is the sample standard deviation of the terms. The rate $1/\sqrt n$ does not depend on the dimension. A grid with $n$ points in $d$ dimensions has only $n^{1/d}$ points per axis, and the midpoint rule's error grows like $n^{-2/d}$: better than Monte Carlo in one or two dimensions, worse beyond four.

:::edge{from=M17 text="Monte Carlo is integration by sampling."}
:::

To reduce the variance without more samples: **control variates** subtract a correlated quantity with a known mean, and **importance sampling**, next, puts the samples where they matter.

::::derivation{id=d4 title="Pi by darts"}
:::step
Throw $n = 10^6$ darts uniformly into the unit square; the fraction inside the quarter circle estimates $\pi/4$. Each dart is a Bernoulli with $p = \pi/4$, so four times the fraction has standard error $4\sqrt{p(1 - p)/n} \approx$ [[0.00164|tol=0.00002]].
:::
:::step
To gain one more correct decimal digit, multiply the number of darts by [[100]].
:::
::::

## 5. Importance sampling

To estimate $\mathbb{E}_p[f(X)]$ when $f$ matters only where $p$ is small, sample from another density $q$ and reweight:

$$
\mathbb{E}_p[f(X)] = \int f\,\frac{p}{q}\,q\,dx = \mathbb{E}_q\big[f(X)\,w(X)\big], \qquad w = \frac{p}{q} .
$$

The estimator is unbiased whenever $q > 0$ wherever $fp \ne 0$. Its variance is $\mathbb{E}_q[f^2w^2] - (\mathbb{E}_pf)^2$, small when $q$ is roughly proportional to $\lvert f\rvert p$ and infinite when $q$'s tails are much lighter than $fp$'s: the weights $p/q$ explode exactly where $q$ almost never samples. The **effective sample size** $(\sum w)^2/\sum w^2$ diagnoses it.

For $P(Z > a)$ with $Z$ standard normal, sampling from $N(\theta, 1)$ gives weights $w(x) = e^{-\theta x + \theta^2/2}$, and a shift $\theta$ near $a$ turns a one-in-a-million event into a coin flip.

::::derivation{id=d5 title="A rare tail"}
:::step
$P(Z > 4) \approx 3.17 \times 10^{-5}$. A naive sampler has relative standard error $\sqrt{(1 - p)/(np)}$; for 10 percent it needs $n \approx 100/p \approx$ [[3.16e6|tol=0.05e6]] samples.
:::
:::step
With the proposal $N(4, 1)$, a sample at $x = 4$ carries the weight $e^{-16 + 8} = e^{-8} \approx$ [[0.000335|tol=0.000003]].
:::
::::

The same reweighting computes gradients of expectations, the subject of M36.

:::edge{to=M36 text="Monte Carlo returns as gradient estimation."}
:::

:::edge{to=M25 text="estimators, their sampling distributions and the bootstrap."}
:::

:::edge{to=M31 text="concentration inequalities sharper than Chebyshev's."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Markov | $P(X \ge a) \le \mathbb{E}X/a$ for $X \ge 0$ | crude tail bound |
| Chebyshev | $P(\lvert X - \mu\rvert \ge \varepsilon) \le \sigma^2/\varepsilon^2$ | tail bound from a variance |
| Law of large numbers | $\bar X_n \to \mu$ in probability | averages settle |
| Central limit theorem | $(\bar X_n - \mu)\sqrt n/\sigma \to N(0, 1)$ | intervals $\bar x \pm 1.96\,s/\sqrt n$ |
| MGF | $M'(0) = \mathbb{E}X$; sums multiply MGFs | moments, the CLT proof |
| Monte Carlo | estimate $=$ average, SE $= s/\sqrt n$ | integrals in any dimension |
| Importance sampling | $\mathbb{E}_p f = \mathbb{E}_q[f\,p/q]$ | rare events, variance reduction |
