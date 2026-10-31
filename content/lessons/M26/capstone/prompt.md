# Capstone: a numerically hardened library

Write a small library of the functions every training loop calls, and make each survive extreme inputs. The tests are an adversarial suite of **40 cases**: logits of $\pm 1000$, $\pm 10^{308}$ and $-\infty$, probabilities a hair from 1, data with means of $10^{15}$, and sums that cancel. On a desktop they run with NumPy set to raise an error on any overflow, invalid operation or division by zero (underflow to 0 is allowed); the browser's NumPy cannot detect these events, so there the 40 values alone decide, and an implementation that overflows on the way to a right answer slips through. Write it as if the traps were always on.

1. `logsumexp(z)`, `softmax(z)` and `log_softmax(z)` along the last axis. If every entry is $-\infty$, log-sum-exp is $-\infty$: take the logarithm of the zero sum inside `np.errstate(divide="ignore")`.
2. `sigmoid(x)`, `softplus(x)` and `log_sigmoid(x)`, elementwise.
3. `cross_entropy(logits, labels)`: the mean of $-\log\operatorname{softmax}$ over a batch of rows, and `bce_with_logits(x, y)`: the binary cross-entropy $\max(x, 0) - xy + \log(1 + e^{-\lvert x\rvert})$, elementwise.
4. `mean_var(x)`: the mean and the variance with $n - 1$, accurate for data far from 0.
5. `log1mexp(a)`: $\log(1 - e^{-a})$ for $a > 0$: use $\log(-\operatorname{expm1}(-a))$ for $a < \log 2$ and $\operatorname{log1p}(-e^{-a})$ otherwise.
6. `compensated_sum(x)`: Neumaier's variant of Kahan summation in float64: with running sum $s$ and correction $c$, for each $x$ form $t = s + x$; add $(s - t) + x$ to $c$ if $\lvert s\rvert \ge \lvert x\rvert$, else $(x - t) + s$; set $s = t$; return $s + c$. Unlike plain Kahan, it survives $[10^{16}, 1, -10^{16}]$.
