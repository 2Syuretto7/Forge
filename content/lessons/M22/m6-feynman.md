# Explain it plainly: why variances add

Explain why the variance of a sum of independent pieces adds, and what that says about initialization.

Guidelines:

- Write 150 to 400 words.
- Start from the variance of a sum of two pieces.
- Say where independence is used.
- Finish with the weight scale for a layer with many inputs.

:::feynman{id=f1 prompt="Explain why the variance of a sum of independent pieces adds, and what that says about initialization." key_points="Expands the squared deviation of a sum into the two squared deviations plus a cross term|The cross term is twice the covariance, which is zero for independent pieces, so the variances add|The standard deviation therefore grows like the square root of the number of pieces, because the pieces partly cancel|A neuron sums n weight-times-input terms, so its output variance is n times the variance of one term|To keep the variance from growing or shrinking layer after layer, the weight variance must be about 1/n (2/n with ReLU)"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that if X and Y are independent random variables with finite variances, then Var(X + Y) = Var X + Var Y." key_points="Writes the mean of X + Y as the sum of the means by linearity|Expands (X + Y - mean of X - mean of Y) squared into the two squared deviations and twice their product|Takes expectations term by term by linearity, so the cross term is 2 Cov(X, Y)|Uses independence: E[XY] = E[X] E[Y], so Cov(X, Y) = 0|Concludes Var(X + Y) = Var X + Var Y"}
:::
