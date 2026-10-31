# Puzzle: a gradient through a coin flip

A language model samples a token, a reward model scores the result, and you want to change the weights so that the expected score rises. The sampling step is a discrete choice: a tiny change of the weights either leaves the token the same or switches it, so the derivative of the sampled token with respect to the weights is zero almost everywhere.

::::predict{id=p1 kind=choice answer=c}
Can you still get an unbiased estimate of the gradient of the expected reward from samples?

- No: the gradient is zero almost everywhere, so the expected reward cannot be improved by gradients.
- Only by replacing the discrete choice with a continuous one.
- Yes: weight the gradient of the log-probability of each sampled action by its reward.
- Only by computing the reward of every possible token.

:::reveal
Yes. The expected reward is a smooth function of the probabilities even though each sample is not, and its gradient is $\mathbb{E}[r\,\nabla\log\pi(a)]$, an expectation that samples estimate without bias. The derivation is two lines; the hard part, which most of this lesson is about, is the variance.
:::
::::

::::predict{id=p2 kind=numeric answer=0.5 tol=0.05}
A coin policy takes action 1 with probability $p = \sigma(\theta)$, currently $\frac12$; action 1 earns reward 3 and action 0 earns 1. What is the derivative of the expected reward with respect to $\theta$?

:::reveal
$0.5$: the expected reward is $3p + (1 - p) = 1 + 2p$, and $dp/d\theta = p(1 - p) = \frac14$, so the derivative is $2 \times \frac14$. The log-derivative trick recovers it as $\mathbb{E}[r(x - p)] = \frac12 \cdot 3 \cdot \frac12 - \frac12 \cdot 1 \cdot \frac12$.
:::
::::

## Questions to carry into the derivation

1. How can an expectation over discrete samples have a usable gradient?
2. Why is the obvious estimator so noisy, and what reduces the noise for free?
3. When can the gradient pass through the sample instead?
4. How do these estimators extend from one decision to a sequence of them?
