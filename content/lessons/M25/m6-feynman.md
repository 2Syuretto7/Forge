# Explain it plainly: the likelihood

Explain what the likelihood measures and why it is not a probability over the parameter.

Guidelines:

- Write 150 to 400 words.
- Use a coin flipped a few times as the example.
- Say what you would need to turn it into a probability over the parameter.
- Say what its peak and its curvature tell you.

:::feynman{id=f1 prompt="Explain what the likelihood measures and why it is not a probability over the parameter." key_points="The likelihood of a parameter value is the probability of the observed data if that value were true|It is a function of the parameter with the data held fixed, and it need not integrate to 1 over the parameter|Its maximum is the maximum-likelihood estimate, the value under which the data were most probable|The curvature at the peak measures how sharply the data pin down the parameter, giving a standard error|To get a probability distribution over the parameter you need a prior and Bayes' rule, which normalizes likelihood times prior"}
:::

## A written proof

:::feynman{id=proof1 prompt="For n independent coin flips with k heads, prove that the maximum-likelihood estimate of the probability of heads is k/n, and that a Beta(a, b) prior gives a Beta(a + k, b + n - k) posterior." key_points="Writes the likelihood as p^k (1 - p)^(n - k), the product over independent flips|Takes the logarithm and sets its derivative k/p - (n - k)/(1 - p) to zero to get p = k/n|Checks that the second derivative is negative, so it is a maximum (or handles k = 0 and k = n at the boundary)|Multiplies the likelihood by the prior density proportional to p^(a - 1) (1 - p)^(b - 1)|Recognizes p^(a + k - 1) (1 - p)^(b + n - k - 1) as an unnormalized Beta(a + k, b + n - k) density"}
:::
