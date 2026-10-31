# Recall bridge: from probability to surprise

M21 measured how evidence changes beliefs, M22 averaged functions of random variables, and M25 fitted models by maximizing the log-likelihood. This lesson gives the logarithm of a probability its own name, surprise, and builds from it the quantities in every training log: entropy, cross-entropy, KL divergence and perplexity. Clear your due cards above first.

:::edge{from=M22 text="expectation, now of the surprisal"}
:::

:::edge{from=M21 text="the surprise of an event is minus the log of its probability"}
:::

:::edge{from=M06 text="logarithms turn products into sums"}
:::

## What carries over

From M06, $\log(ab) = \log a + \log b$ and changes of base, $\log_2 x = \ln x/\ln 2$. From M22, $\mathbb{E}[g(X)] = \sum_x p(x)g(x)$. From M25, the average log-likelihood $\frac1n\sum_i \log q(x_i)$ and its maximizer $q_j = c_j/n$ for categorical data. From M19, the softmax and its Jacobian $\operatorname{diag}(p) - pp^\top$.
