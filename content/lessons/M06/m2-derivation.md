# Derivation: from powers to the exponential and the logarithm

## 1. Extending the exponent

Start with positive $a$ and integer powers, where $a^n$ means $n$ factors of $a$. Keep the rule $a^m a^n = a^{m+n}$ true at every step.

- $a^0$: since $a^0 a^n = a^n$, we need $a^0 = 1$.
- Negative powers: $a^{-n} a^n = a^0 = 1$, so $a^{-n} = 1/a^n$.
- Fractions: $(a^{1/n})^n = a^{(1/n) \cdot n} = a$, so $a^{1/n}$ must be the positive number whose $n$-th power is $a$: the $n$-th root. And $a^{p/q} = (a^{1/q})^p$.
- Irrational exponents such as $2^\pi$: approximate $\pi$ by fractions $3, 3.1, 3.14, 3.141, \dots$ The powers $2^3, 2^{3.1}, 2^{3.14}, \dots$ form a sequence that converges (M05), and $2^\pi$ is its limit.

::::derivation{id=d1 title="Fractional and negative exponents"}
:::step
$8^{1/3}$ is the number whose cube is 8, which is [[2]].
:::
:::step
$8^{2/3} = (8^{1/3})^2 =$ [[4]].
:::
:::step
$2^{-3} = 1 / 2^3 =$ [[1/8]].
:::
:::step
With the rule $(a^m)^n = a^{mn}$ also kept, $(2^{1/2})^4 = 2^{\,?}$, which is [[4]].
:::
::::

The function $x \mapsto a^x$ is an **exponential** function with base $a$. For $a > 1$ it increases, faster than any power of $x$ in the end, and every output is positive.

## 2. The number e

Put money in a bank at 100 percent interest a year. Compounded once, 1 becomes 2. Compounded twice (50 percent each half year), $1.5^2 = 2.25$. Monthly, $(1 + \frac{1}{12})^{12} \approx 2.613$. Daily, $\approx 2.7146$. Does it grow without limit?

It does not. The sequence $(1 + \frac{1}{n})^n$ increases and converges to a constant,

$$
e = \lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n = 2.718281828\ldots
$$

With a rate $x$ instead of 100 percent, $(1 + \frac{x}{n})^n \to e^x$. Expanding with the binomial theorem (M08) and letting $n \to \infty$ gives a second description, the series

$$
e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \dots ,
$$

which converges for every $x$, fast: for $x = 1$, fifteen terms give twelve correct digits, while compounding a million times gives only six.

::::derivation{id=d2 title="Continuous growth"}
:::step
Compounding 5 percent a year continuously for 10 years multiplies by $e^{0.05 \times 10} = e^{0.5} \approx$ [[1.6487|tol=0.001]].
:::
:::step
Something growing continuously at rate $r$ doubles when $e^{rt} = 2$, that is after $t = \ln 2 / r$, where $\ln$ is the inverse of $e^x$ (Section 3). At $r = 0.07$ per year, the doubling time is about [[ln(2)/0.07|tol=0.05]] years.
:::
::::

That is the "rule of 70": at $r$ percent a year, doubling takes about $70/r$ years, because $\ln 2 \approx 0.693$.

## 3. The logarithm

$e^x$ is increasing and its outputs are exactly the positive numbers, so by M04 it has an inverse. That inverse is the **natural logarithm** $\ln$:

$$
y = e^x \iff x = \ln y \qquad (y > 0) .
$$

More generally $\log_b y$ is the inverse of $b^x$: the power of $b$ that gives $y$. So $\log_{10} 1000 = 3$ and $\log_2 1024 = 10$. A logarithm **is** an exponent.

Every rule of logarithms is a power rule read backwards.

::::derivation{id=d3 title="The logarithm rules from the power rules"}
:::step
Let $u = \log_b x$ and $v = \log_b y$, so $x = b^u$ and $y = b^v$. Then $xy = b^u b^v = b^{u+v}$, so $\log_b(xy) =$ [[u + v]].
:::
:::step
Similarly $x^k = (b^u)^k = b^{ku}$, so $\log_b(x^k) = k \log_b x$. With $\log_{10} 2 \approx 0.301$, $\log_{10}(2^{10}) \approx$ [[3.01|tol=0.005]], which is why $2^{10}$ is close to $10^3$.
:::
:::step
**Change of base:** from $x = b^{\log_b x}$, take $\ln$ of both sides: $\ln x = \log_b x \cdot \ln b$. So $\log_2 1000 =$ [[ln(1000)/ln(2)]], about 9.97.
:::
::::

:::edge{to=M27 text="information is measured in logarithms: the surprise of an event is minus the log of its probability, in bits for base 2 and nats for base e."}
:::

**Log scales.** On a logarithmic axis, equal distances mean equal factors. That is how M01's ladder of powers of ten was drawn. Three consequences, which the puzzle used:

| Data straight on | Law | Parameters |
| --- | --- | --- |
| linear axes | $y = a + bx$ | slope $b$ |
| $\log y$ against $x$ (semi-log) | exponential $y = a\,c^x$ | slope $\log c$ |
| $\log y$ against $\log x$ (log-log) | power law $y = a\,x^p$ | slope $p$ |

::::predict{id=p3 kind=choice answer=a}
Which is larger, $2^{100}$ or $100^{10}$?

- $2^{100}$, by a factor of about $10^{10}$.
- $100^{10}$, by a factor of about $10^{10}$.
- They are equal.
- They are within a factor of 2.

:::reveal
Compare logarithms: $\log_{10} 2^{100} = 100 \times 0.301 = 30.1$ and $\log_{10} 100^{10} = 10 \times 2 = 20$. So $2^{100} \approx 1.27 \times 10^{30}$ dwarfs $100^{10} = 10^{20}$ by about $10^{10}$. Exponentials beat powers, and logarithms are how you compare numbers too big to write down.
:::
::::

## 4. Functions built from the exponential

**The sigmoid** $\sigma(x) = \dfrac{1}{1 + e^{-x}}$ squashes any real number into $(0, 1)$: very negative inputs give nearly 0, very positive nearly 1, and $\sigma(0) = \frac{1}{2}$. It is symmetric in the sense $\sigma(-x) = 1 - \sigma(x)$, and its inverse is the **logit** $\ln \frac{p}{1 - p}$. Logistic regression (L05) is built on it.

**The softmax** turns a list of real numbers $z_1, \dots, z_n$ (scores, "logits") into probabilities:

$$
\operatorname{softmax}(z)_i = \frac{e^{z_i}}{\sum_j e^{z_j}} .
$$

Each output is positive, they sum to 1, and larger scores get larger probabilities. The sigmoid is a two-class softmax: $\sigma(x) = \operatorname{softmax}(x, 0)_1$. Every language model ends with a softmax over its vocabulary.

**Log-sum-exp** $\operatorname{LSE}(z) = \ln \sum_j e^{z_j}$ is a smooth version of the maximum: it is at least $\max_j z_j$ and at most $\max_j z_j + \ln n$. The log of a softmax output is $z_i - \operatorname{LSE}(z)$.

::::derivation{id=d4 title="Shifting the scores changes nothing, and saves everything"}
:::step
Subtract the same number $c$ from every score: $\dfrac{e^{z_i - c}}{\sum_j e^{z_j - c}} = \dfrac{e^{-c}\, e^{z_i}}{e^{-c} \sum_j e^{z_j}}$, and the factors $e^{-c}$ cancel. So the softmax is unchanged by the shift. Choosing $c = \max_j z_j$, the largest exponential that is computed is $e^0 =$ [[1]].
:::
:::step
For log-sum-exp the shift comes out of the logarithm: $\operatorname{LSE}(z) = c + \ln \sum_j e^{z_j - c}$. For $z = (1000, 1000)$, $\operatorname{LSE}(z) =$ [[1000 + ln(2)]].
:::
:::step
With $c = \max z$, every $e^{z_j - c}$ is at most 1 and one of them equals 1, so the sum lies between 1 and $n$. Hence $\max z \leq \operatorname{LSE}(z) \leq \max z + \ln n$; for $n = 50{,}000$ the gap is at most $\ln 50000 \approx$ [[10.82|tol=0.01]].
:::
::::

That shift is the most important line of numerical code in machine learning. $e^{1000}$ overflows every floating-point format, but $e^{1000 - 1000} = 1$ does not. You will break the naive softmax in Movement 5 and fix it with this derivation.

:::edge{to=M15 text="the exponential is the function equal to its own derivative, which is where e really comes from."}
:::

:::edge{to=M26 text="floating point stores numbers as mantissa times a power of two; the max shift becomes a general lesson in stability."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Powers | $a^0 = 1$, $a^{-n} = 1/a^n$, $a^{p/q} = (a^{1/q})^p$ | any real exponent |
| $e$ | $\lim (1 + 1/n)^n = \sum 1/k! = 2.71828\ldots$ | continuous growth |
| Logarithm | inverse of the exponential; $\log(xy) = \log x + \log y$ | multiply by adding |
| Log axes | straight on semi-log: exponential; on log-log: power law | reading growth laws |
| Softmax | $e^{z_i} / \sum_j e^{z_j}$, unchanged by shifting $z$ | probabilities from scores |
| Log-sum-exp | $c + \ln \sum e^{z_j - c}$ with $c = \max z$ | stable log-probabilities |
