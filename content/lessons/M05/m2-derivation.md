# Derivation: sequences, sums, induction and growth

## 1. Sequences and their limits

A **sequence** is a function of the whole numbers: $a_1, a_2, a_3, \dots$, or $a_n$ for short. Examples: $a_n = 1/n$; $a_n = (-1)^n$; $a_n = r^n$.

Informally, $a_n$ has **limit** $L$ if the terms get and stay as close to $L$ as you like. Precisely:

$$
\lim_{n \to \infty} a_n = L \quad \text{means} \quad \text{for every } \varepsilon > 0 \text{ there is an } N \text{ such that } |a_n - L| < \varepsilon \text{ for every } n > N .
$$

Read it with M03's quantifiers: for every tolerance $\varepsilon$ (however small) there is a point $N$ (which may depend on $\varepsilon$) after which every term is within $\varepsilon$ of $L$. It is a "for every, there exists, for every" statement, and to verify it you give a recipe for $N$ in terms of $\varepsilon$.

::::derivation{id=d1 title="Finding N for a given tolerance"}
:::step
For $a_n = 1/n$ and $L = 0$, $|a_n - 0| < \varepsilon$ means $n > 1/\varepsilon$. For $\varepsilon = 0.001$ you can take $N =$ [[1000]].
:::
:::step
For $a_n = r^n$ with $0 < r < 1$, $r^n < \varepsilon$ means $n \ln r < \ln \varepsilon$. Since $\ln r < 0$, dividing flips the inequality: $n > \ln \varepsilon / \ln r$. For $r = 0.9$ and $\varepsilon = 10^{-6}$, the first $n$ that works is [[132|tol=1]].
:::
:::step
The sequence $(-1)^n$ jumps between $-1$ and $1$ forever. For $\varepsilon = 0.5$, can any $N$ make every later term within 0.5 of a single $L$? Answer yes or no: [[word:no]].
:::
::::

(The logarithm appears here a lesson early; M06 builds it. For now, $\ln$ is the inverse of the exponential, and it turns "how many factors of $r$" into a division.)

A sequence with a limit **converges**; one without **diverges**. Convergence is a "for every $\varepsilon$" statement, so no finite table of terms proves it; a counterexample (a tolerance no $N$ achieves) disproves it.

## 2. Sums and sigma notation

The sum $a_1 + a_2 + \dots + a_n$ is written

$$
\sum_{k=1}^{n} a_k .
$$

The letter $k$ is a dummy: renaming it changes nothing. Sums obey the field rules of M02 term by term: $\sum (a_k + b_k) = \sum a_k + \sum b_k$ and $\sum c\, a_k = c \sum a_k$. That is **linearity**, and it is the single most used fact about sums.

**Arithmetic series.** Carl Friedrich Gauss, as a schoolboy, is said to have added $1 + 2 + \dots + 100$ by pairing the first and last terms.

::::derivation{id=d2 title="Adding 1 to n by pairing"}
:::step
Write $S = 1 + 2 + \dots + n$ forwards and backwards and add: each of the $n$ columns sums to $n + 1$, so $2S = n(n + 1)$. For $n = 100$, $S =$ [[5050]].
:::
:::step
In general, $\displaystyle\sum_{k=1}^{n} k =$ [[n*(n + 1)/2]].
:::
:::step
The sum of the first $n$ odd numbers, $1 + 3 + \dots + (2n - 1)$, is $2 \sum k - n = n(n + 1) - n =$ [[n^2]].
:::
::::

**Geometric series.** Multiply the sum by the ratio and subtract.

::::derivation{id=d3 title="The geometric series"}
:::step
Let $S_n = 1 + r + r^2 + \dots + r^{n-1}$. Then $r S_n = r + r^2 + \dots + r^n$, and subtracting, everything cancels except $r S_n - S_n = r^n - 1$. So for $r \neq 1$, $S_n =$ [[(r^n - 1)/(r - 1)]].
:::
:::step
If $|r| < 1$, then $r^n \to 0$, so $S_n \to$ [[1/(1 - r)]].
:::
:::step
For $r = \frac{1}{2}$ the infinite sum is [[2]], the puzzle's answer.
:::
::::

So an infinite sum is defined as the limit of its partial sums, when that limit exists. The geometric series converges for $|r| < 1$ and diverges otherwise.

:::edge{to=M29 text="an optimizer whose error shrinks by a factor r each step converges like a geometric series: linear convergence, with about ln(1/eps)/ln(1/r) steps to reach eps."}
:::

## 3. Induction

How do you prove $1 + 3 + \dots + (2n - 1) = n^2$ for **every** $n \geq 1$, not just the ones you tested? **Induction** proves $P(n)$ for every $n \geq n_0$ from two parts:

1. **Base case:** $P(n_0)$ is true.
2. **Step:** for every $n \geq n_0$, if $P(n)$ is true then $P(n + 1)$ is true.

Why that suffices: suppose $P$ failed somewhere. Take the smallest failure $m$. It is not $n_0$ (the base case holds), so $m - 1 \geq n_0$ and $P(m - 1)$ holds (since $m$ was the smallest failure). The step then gives $P(m)$: contradiction. The dominoes picture is the same argument: the first falls, and each knocks over the next.

The horses failed because the step did not work at $n = 1$: "for every $n \geq n_0$" really means every.

::::derivation{id=d4 title="Proving the sum of odd numbers by induction"}
:::step
Base case: for $n = 1$ the left side is just the first odd number, so it equals [[1]], which is $1^2$.
:::
:::step
Step: assume $1 + 3 + \dots + (2n - 1) = n^2$. Adding the next odd number $2n + 1$ gives $n^2 + 2n + 1 =$ [[(n + 1)^2]], which is the claim for $n + 1$.
:::
::::

Notice what induction needs: a formula to prove. It is a way to verify a guess, not to find one. You find the guess by computing small cases (or pairing, or the geometric trick) and then prove it.

## 4. The harmonic series diverges

Group the terms: $1 + \frac{1}{2} + \left(\frac{1}{3} + \frac{1}{4}\right) + \left(\frac{1}{5} + \dots + \frac{1}{8}\right) + \left(\frac{1}{9} + \dots + \frac{1}{16}\right) + \dots$

Each bracket has twice as many terms as the last, and each term in it is at least the bracket's last term. The bracket from $\frac{1}{2^{k-1} + 1}$ to $\frac{1}{2^k}$ has $2^{k-1}$ terms each at least $\frac{1}{2^k}$, so it adds at least $\frac{1}{2}$.

::::derivation{id=d5 title="Grouping the harmonic series"}
:::step
After the first term and $k$ brackets you have added $2^k$ terms, and the sum is at least $1 + \frac{k}{2}$. For $2^{20} \approx$ a million terms, the bound says the sum is at least [[11]].
:::
:::step
Since $1 + \frac{k}{2}$ grows without limit, so do the harmonic sums: the series [[word:diverges]].
:::
::::

The true growth is $\ln n + 0.5772\ldots$ (the constant is the Euler-Mascheroni constant $\gamma$), which you can derive with the integrals of M17. Divergence this slow is why no table of partial sums would ever have convinced you.

## 5. Growth and the cost of algorithms

The running time of an algorithm is a sum: one term per step. A loop that does constant work $n$ times costs about $n$; two nested loops over $i < j$ cost $\binom{n}{2} = \frac{n(n-1)}{2}$.

We compare growth with **big-O** notation: $f(n) = O(g(n))$ means $f(n) \leq C g(n)$ for some constant $C$ and every large $n$. Constants and lower-order terms are ignored: $\frac{n(n-1)}{2} = O(n^2)$, and $3n + 7 = O(n)$.

::::predict{id=p3 kind=choice answer=c}
How many times does the body run in `for i in range(n): for j in range(i): for k in range(j): body()`?

- $n^3$
- $\frac{n^3}{2}$
- $\binom{n}{3} = \frac{n(n-1)(n-2)}{6}$, which is about $\frac{n^3}{6}$.
- $3n$

:::reveal
The body runs once for each triple $k < j < i$ of distinct indices below $n$, and there are $\binom{n}{3}$ such triples, about $n^3/6$. It is still $O(n^3)$: doubling $n$ multiplies the work by about 8. The exact constant matters for running time; the exponent matters for how it scales.
:::
::::

A reliable way to read the exponent from measurements: if the cost is about $C n^p$, then doubling $n$ multiplies it by $2^p$, and on log-log axes the points lie on a line of slope $p$. You will measure exactly that.

:::edge{to=M15 text="the limit of a sequence becomes the limit of a function, and the derivative is defined as one."}
:::

:::edge{to=M06 text="the exponential is a limit of compounding, and log n is how fast the harmonic sums grow."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Limit | for every $\varepsilon$ there is $N$ with $\lvert a_n - L \rvert < \varepsilon$ for $n > N$ | convergence of anything |
| Arithmetic series | $\sum_{k=1}^n k = n(n+1)/2$ | counting pairs |
| Geometric series | $\sum_{k=0}^{n-1} r^k = (r^n - 1)/(r - 1)$, limit $1/(1 - r)$ | convergence rates (M29) |
| Induction | base case and a step for every $n$ | proving formulas |
| Harmonic series | diverges, like $\ln n$ | slow growth |
| Big-O | ignore constants; doubling $n$ multiplies $n^p$ by $2^p$ | algorithm cost |
