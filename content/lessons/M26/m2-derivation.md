# Derivation: floating point and numerical stability

## 1. Binary floating point

A floating-point number is a sign, a binary fraction and a power of two:

$$
x = (-1)^s \times 1.f_1 f_2 \dots f_p \times 2^{e} .
$$

**Float32** spends 1 bit on $s$, 8 on the exponent (stored with a bias of 127) and $p = 23$ on the fraction, for 24 significant bits counting the implicit leading 1. **Float64** has 11 and 52. Between consecutive powers of two the floats are evenly spaced, with gap $2^{e - p}$: the gap doubles at each power of two, so floats are dense near 0 and sparse far away. Exponent fields of all zeros hold the **subnormals**, which fill the gap down to 0, and all ones hold $\pm\infty$ and NaN.

::::derivation{id=d1 title="Gaps between float32 numbers"}
:::step
Just above 1 the gap is $2^{-23} \approx$ [[1.19e-7|tol=0.01e-7]].
:::
:::step
Between $2^{24}$ and $2^{25}$ the gap is [[2]], which is why adding 1 to $2^{24}$ does nothing.
:::
::::

## 2. Rounding and machine epsilon

Every arithmetic operation computes the exact result and rounds it to the nearest float (ties to even). So for $\circ$ any of $+, -, \times, \div$,

$$
\operatorname{fl}(a \circ b) = (a \circ b)(1 + \delta), \qquad \lvert\delta\rvert \le u = 2^{-(p + 1)} .
$$

The **machine epsilon** $\varepsilon = 2^{-p}$ is the gap between 1 and the next float, and the **unit roundoff** $u = \varepsilon/2$ the largest relative error of one rounding: about $6 \times 10^{-8}$ in float32 and $1.1 \times 10^{-16}$ in float64. Each operation is accurate; the trouble comes from what later operations do with the tiny errors. Formats for deep learning trade fraction bits for range or memory: **fp16** keeps 10 fraction bits, **bf16** keeps 7 with float32's exponent range, and **fp8** keeps 2 or 3.

::::derivation{id=d2 title="Epsilons of the small formats"}
:::step
fp16 has 10 fraction bits: $\varepsilon = 2^{-10} \approx$ [[0.000977|tol=0.000002]].
:::
:::step
bf16 has 7: $\varepsilon = 2^{-7} =$ [[0.0078125|tol=0.00001]], so it cannot tell 1 from $1.003$.
:::
::::

:::edge{to=L13 text="machine epsilon returns as the limits of bf16 and fp8."}
:::

## 3. Catastrophic cancellation

Subtracting two nearly equal numbers is exact (for floats within a factor of 2 of each other), but it exposes the errors they already carried. If $\tilde a = a(1 + \delta_a)$ and $\tilde b = b(1 + \delta_b)$, then

$$
\frac{\lvert(\tilde a - \tilde b) - (a - b)\rvert}{\lvert a - b\rvert} \le \frac{\lvert a\rvert + \lvert b\rvert}{\lvert a - b\rvert}\,\max(\lvert\delta_a\rvert, \lvert\delta_b\rvert) :
$$

the relative error is amplified by the ratio of the size of the inputs to the size of the result. The leading digits cancel and the trailing digits, which were rounding noise, become the answer.

The remedy is algebra before arithmetic: rewrite the formula so that it never subtracts nearly equal computed quantities. $1 - \cos x = 2\sin^2(x/2)$; $e^x - 1$ and $\log(1 + x)$ for small $x$ have their own library functions, `expm1` and `log1p`; the variance is the mean squared deviation from the mean, not the mean square minus the squared mean; the small root of a quadratic is $c/q$ where $q$ is computed without cancellation.

::::derivation{id=d3 title="One minus a cosine"}
:::step
$\cos(10^{-4}) = 1 - 5 \times 10^{-9} + \dots$. In float32, where the gap below 1 is $6 \times 10^{-8}$, it rounds to 1, and $1 - \cos(10^{-4})$ computes as [[0]].
:::
:::step
$2\sin^2(5 \times 10^{-5})$ involves no subtraction and gives $\approx$ [[5e-9|tol=0.1e-9]], correct to float32 precision.
:::
::::

::::predict{id=p3 kind=numeric answer=6 tol=1}
In float64, about how many correct significant digits does the computed value of $(1 + 10^{-10}) - 1$ have?

:::reveal
About 6. Storing $1 + 10^{-10}$ makes an absolute error up to $1.1 \times 10^{-16}$; the subtraction keeps that error but shrinks the value to $10^{-10}$, so the relative error is about $10^{-6}$. Sixteen digits went in, six came out: the ten leading digits of $1.0000000001$ cancelled.
:::
::::

## 4. Conditioning and stability

Two different things can go wrong, and they must not be confused.

A **problem** is **ill-conditioned** when small changes in its input cause large changes in its exact answer. Its relative **condition number** is $\kappa = \lvert x f'(x)/f(x)\rvert$ for a function, and $\kappa(A) = \sigma_{\max}/\sigma_{\min}$ for solving $Ax = b$. Subtraction $a - b$ has $\kappa = (\lvert a\rvert + \lvert b\rvert)/\lvert a - b\rvert$: cancellation is ill-conditioning.

An **algorithm** is **backward stable** when its computed answer is the exact answer for an input within a few rounding errors of the true one. Then

$$
\text{relative forward error} \lesssim \kappa \times u .
$$

A stable algorithm on an ill-conditioned problem loses $\log_{10}\kappa$ digits, and nothing can do better, because the input itself was stored with error $u$. An unstable algorithm can lose digits even on a perfectly conditioned problem: the naive variance formula, or elimination with a tiny pivot. Gaussian elimination with partial pivoting is backward stable in practice; without pivoting it is not.

:::edge{from=M11 text="pivoting is a stability choice, not only an algebra step."}
:::

::::derivation{id=d4 title="Conditioning of a logarithm"}
:::step
$f(x) = \log x$ has $\kappa = \lvert x \cdot \frac1x / \log x\rvert = 1/\lvert\log x\rvert$. At $x = 1.001$ that is about [[1000|tol=5]].
:::
:::step
So any algorithm loses about [[3]] decimal digits computing $\log(1.001)$ from a stored $1.001$, which is why `log1p` takes the small increment itself as input.
:::
::::

## 5. Stable softmax, log-sum-exp and log-sigmoid

The functions at the end of every classifier involve exponentials, which overflow above about 710 in float64 and 89 in float32. Three identities make them safe.

**Log-sum-exp.** With $m = \max_i z_i$,

$$
\log\sum_i e^{z_i} = m + \log\sum_i e^{z_i - m} .
$$

Every exponent is now at most 0, so nothing overflows, and the largest term is $e^0 = 1$, so the sum is at least 1 and its logarithm cannot be $-\infty$. **Softmax** is $e^{z - \operatorname{lse}(z)}$, and **log-softmax** $z - \operatorname{lse}(z)$, never the logarithm of a computed probability.

**Softplus and log-sigmoid.** $\operatorname{softplus}(x) = \log(1 + e^x) = \max(x, 0) + \log(1 + e^{-\lvert x\rvert})$, with `log1p`; $\log\sigma(x) = -\operatorname{softplus}(-x)$; and $\sigma(x)$ from $e^{-\lvert x\rvert}$, which never overflows. Binary cross-entropy from a logit is $\max(x, 0) - xy + \log(1 + e^{-\lvert x\rvert})$.

The rule behind all of them: **keep log-probabilities in log space**. A probability of $e^{-1000}$ is 0 in any format, but its logarithm, $-1000$, is an ordinary number.

::::derivation{id=d5 title="Logits of a thousand"}
:::step
$\operatorname{lse}(1000, 1000) = 1000 + \log 2 \approx$ [[1000.693|tol=0.001]], although $e^{1000}$ overflows.
:::
:::step
$\log\sigma(-1000) = -\operatorname{softplus}(1000) =$ [[-1000]], although $\sigma(-1000)$ underflows to 0.
:::
::::

## 6. Summing many numbers

A sequential sum of $n$ numbers can accumulate an error up to about $n u \sum\lvert x_i\rvert$: every addition rounds, and late terms are added to a large total whose gap swallows them. Three cures, from cheapest to most accurate:

- **Pairwise summation** adds in a balanced tree; each term meets only $\log_2 n$ roundings, and the bound becomes $u\log_2 n\sum\lvert x_i\rvert$. NumPy's `sum` does this inside.
- **Kahan summation** keeps a compensation $c$, the rounding error of the last addition, computed exactly as $c = (t - s) - y$, and subtracts it from the next term. Its error bound, about $2u\sum\lvert x_i\rvert$, does not grow with $n$. Neumaier's variant also survives terms larger than the running sum.
- **Higher precision** for the accumulator: summing float32 data in a float64 total, the choice of mixed-precision training.

:::edge{from=M24 text="summing a million samples needs compensated summation."}
:::

:::edge{from=M19 text="finite differences fail at tiny steps; automatic differentiation does not."}
:::

:::edge{to=M33 text="numerical linear algebra at scale."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Float format | $(-1)^s\,1.f \times 2^e$, gap $2^{e - p}$ | know what is representable |
| Rounding | $\operatorname{fl}(a \circ b) = (a \circ b)(1 + \delta)$, $\lvert\delta\rvert \le u$ | error per operation |
| Epsilon | $2^{-23}$ float32, $2^{-52}$ float64, $2^{-7}$ bf16 | precision limits |
| Cancellation | error amplified by $(\lvert a\rvert + \lvert b\rvert)/\lvert a - b\rvert$ | rewrite formulas |
| Conditioning | $\kappa = \lvert xf'/f\rvert$, $\sigma_{\max}/\sigma_{\min}$ | digits lost by any method |
| Stability | forward error $\lesssim \kappa u$ for a backward-stable method | trust an algorithm |
| Log-sum-exp | subtract the max; stay in log space | softmax, cross-entropy |
| Summation | pairwise, Kahan, a wider accumulator | long sums |
