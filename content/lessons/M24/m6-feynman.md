# Explain it plainly: the square root law

Explain why error bars shrink like one over the square root of the number of samples.

Guidelines:

- Write 150 to 400 words.
- Start from the variance of a sum of independent terms.
- Say what the error bar of a Monte Carlo estimate measures.
- Say what it costs to gain one more digit.

:::feynman{id=f1 prompt="Explain why error bars shrink like one over the square root of the number of samples." key_points="An estimate built from n independent samples is an average of n terms|Variances of independent terms add, so the sum has variance n sigma^2 and the average sigma^2 / n|The standard deviation, which sets the error bar, is the square root: sigma / sqrt(n)|By the central limit theorem the average is roughly Gaussian, so plus or minus 1.96 standard errors is a 95 percent interval|Halving the error bar takes four times the samples, and one more decimal digit a hundred times"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove Markov's inequality, P(X >= a) <= E[X]/a for a nonnegative random variable X and a > 0, and derive Chebyshev's inequality from it." key_points="Observes that X >= a times the indicator of the event X >= a, at every outcome, because X is nonnegative|Takes expectations, using that the expectation of an indicator is the probability of its event, to get E[X] >= a P(X >= a)|Divides by a|Applies Markov to the nonnegative variable (X - mu)^2 with threshold epsilon^2|Notes that (X - mu)^2 >= epsilon^2 exactly when the absolute deviation is at least epsilon, giving P(deviation >= epsilon) <= sigma^2 / epsilon^2"}
:::
