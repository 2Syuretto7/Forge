# Derivation: concentration and generalization

## 1. Hoeffding's and Chernoff's inequalities

Let $X_1, \dots, X_n$ be independent with $X_i \in [a, b]$ and mean $\mu$. Apply Markov's inequality to $e^{t(S - n\mu)}$ for any $t > 0$, where $S = \sum X_i$:

$$
P(\bar X - \mu \ge \varepsilon) \le e^{-tn\varepsilon}\,\mathbb{E}e^{t(S - n\mu)} = e^{-tn\varepsilon}\prod_i\mathbb{E}e^{t(X_i - \mu)} .
$$

**Hoeffding's lemma** bounds each factor by $e^{t^2(b - a)^2/8}$ for a bounded variable; choosing the best $t$ gives

$$
P(\lvert\bar X - \mu\rvert \ge \varepsilon) \le 2\exp\left(-\frac{2n\varepsilon^2}{(b - a)^2}\right) .
$$

The tail falls exponentially in $n\varepsilon^2$, where Chebyshev's fell like $1/(n\varepsilon^2)$. Read backwards: with probability at least $1 - \delta$, $\lvert\bar X - \mu\rvert < (b - a)\sqrt{\ln(2/\delta)/(2n)}$. For coins, keeping the exact moment generating function instead of the lemma's bound gives **Chernoff's bound**, $P(\bar X \ge a) \le e^{-n\,\mathrm{KL}(a\|p)}$, sharper because $\mathrm{KL}(a\|p) \ge 2(a - p)^2$.

As $d$ grows the same mechanism makes the norm of a random vector concentrate: $\lVert x\rVert^2$ is a sum of $d$ independent terms, so nearly every Gaussian vector in high dimensions has length close to $\sqrt d$.

:::edge{to=M34 text="concentration of measure becomes the geometry of random high-dimensional vectors."}
:::

::::derivation{id=d1 title="Hoeffding in numbers"}
:::step
With $n = 1000$ and $\delta = 0.05$, the guaranteed half-width is $\sqrt{\ln 40/2000} \approx$ [[0.043|tol=0.001]].
:::
:::step
A half-width of $0.01$ at the same confidence needs $n = \lceil\ln 40/(2 \times 10^{-4})\rceil =$ [[18445|tol=1]] examples.
:::
::::

## 2. The union bound and finite classes

If each of $k$ events fails with probability at most $\delta_j$, the chance that any fails is at most $\sum_j\delta_j$: the **union bound**, crude but assumption-free. Apply it to $k$ hypotheses $h$, each with true error $R(h)$ and empirical error $\hat R(h)$ on the same $n$ examples: giving each the budget $\delta/k$,

$$
P\Big(\exists h:\ \lvert\hat R(h) - R(h)\rvert \ge \varepsilon\Big) \le 2k\,e^{-2n\varepsilon^2}, \qquad \varepsilon_k = \sqrt{\frac{\ln(2k/\delta)}{2n}} .
$$

With probability $1 - \delta$, **every** hypothesis in the class has test error within $\varepsilon_k$ of its training error, including the one that training selects, which is what a generalization bound must say. The price of $k$ hypotheses is only $\ln k$.

:::edge{from=M03 text="quantifiers and proof by contradiction return in generalization bounds."}
:::

::::derivation{id=d2 title="A thousand models"}
:::step
For $k = 1000$ models on $n = 1000$ examples at $\delta = 0.05$, $\varepsilon_k = \sqrt{\ln(40{,}000)/2000} \approx$ [[0.073|tol=0.001]], against $0.043$ for one model.
:::
::::

::::predict{id=p3 kind=choice answer=b}
To give 1,000 models the same guaranteed half-width that one model gets from 1,000 examples, how many examples do you need?

- 1,000,000
- About 2,900
- About 31,600
- 1,000

:::reveal
About 2,900: the sample size scales with $\ln(2k/\delta)$, and $\ln(40{,}000)/\ln(40) \approx 2.9$. Evaluating many models is affordable, provided you count them.
:::
::::

## 3. Infinite classes: growth functions, VC dimension, Rademacher

A linear classifier has infinitely many parameter values, but on $m$ points it can produce only finitely many labellings. The **growth function** $\Pi_{\mathcal H}(m)$ counts them, and replacing $k$ by a bound on $\Pi_{\mathcal H}(2m)$ in the union bound (with a symmetrization argument) gives bounds for infinite classes. The **VC dimension** $d$ is the largest $m$ for which all $2^m$ labellings are possible; **Sauer's lemma** then caps the growth function at $\sum_{i=0}^d\binom mi \le (em/d)^d$, a polynomial, so $\ln\Pi$ grows like $d\ln m$ and the gap shrinks like $\sqrt{d\ln n/n}$. Thresholds on a line have VC dimension 1, intervals 2, half-planes in $\mathbb R^2$ 3, and linear classifiers in $\mathbb R^d$ with a bias $d + 1$.

:::edge{from=M08 text="counting returns as the union bound and growth functions."}
:::

The **Rademacher complexity** $\hat{\mathcal R} = \mathbb{E}_\sigma\sup_h\frac1n\sum_i\sigma_ih(x_i)$ measures the same thing more finely: how well the class can correlate with random signs on this very sample. For linear functions with $\lVert w\rVert \le B$ it is at most $\frac Bn\sqrt{\sum_i\lVert x_i\rVert^2}$, which depends on the norm, not the dimension: a reason large models with small weights can generalize.

::::derivation{id=d3 title="Counting labellings"}
:::step
Thresholds $1[x \ge \theta]$ on 10 distinct points produce [[11]] labellings.
:::
:::step
Half-planes shatter some set of 3 points in the plane but no set of 4, so their VC dimension is [[3]].
:::
::::

::::derivation{id=d4 title="A linear class"}
:::step
For $\lVert w\rVert \le 1$ and 100 points of unit norm, the Rademacher bound is $\sqrt{100}/100 =$ [[0.1]].
:::
::::

## 4. The bias-variance decomposition

For squared loss, data $y = f(x) + \text{noise}$ with variance $\sigma^2$, and a predictor $\hat f$ learned from a random training set, expand $(y - \hat f)^2$ around $f(x)$ and $\mathbb{E}\hat f(x)$; the cross terms vanish in expectation, leaving

$$
\mathbb{E}\big[(y - \hat f(x))^2\big] = \sigma^2 + \big(\mathbb{E}\hat f(x) - f(x)\big)^2 + \operatorname{Var}\hat f(x) .
$$

Noise is irreducible; bias falls and variance rises with capacity, classically. Overparameterized models break the classical U-shape: at the interpolation threshold, where the number of parameters equals the number of examples, variance spikes, and beyond it the minimum-norm solution's variance falls again: **double descent**.

::::derivation{id=d5 title="Adding the parts"}
:::step
Noise $0.25$, squared bias $0.04$ and variance $0.11$ give an expected test error of [[0.4]].
:::
::::

:::edge{to=L02 text="concentration bounds put numbers on the generalization gap."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Hoeffding | $P(\lvert\bar X - \mu\rvert \ge \varepsilon) \le 2e^{-2n\varepsilon^2/(b - a)^2}$ | guaranteed intervals |
| Chernoff | $P(\bar X \ge a) \le e^{-n\,\mathrm{KL}(a\|p)}$ | sharper tails for coins |
| Union bound | $P(\cup A_j) \le \sum P(A_j)$; $\varepsilon_k = \sqrt{\ln(2k/\delta)/(2n)}$ | many models at once |
| Growth function | labellings on $m$ points; Sauer: $\sum_{i \le d}\binom mi$ | infinite classes |
| Rademacher | correlation with random signs; $\le B\sqrt{\sum\lVert x\rVert^2}/n$ | norm-based capacity |
| Bias-variance | noise $+$ bias$^2$ $+$ variance | capacity tradeoffs, double descent |
