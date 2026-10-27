# Build: estimation from scratch

Eight exercises turn the derivation into tools you will reuse for the rest of the course: moments, samplers, Bayes' rule, maximum likelihood for coins, Gaussians and categorical variables, conjugate priors, and a measured estimator bias. Three of them check a gradient against finite differences.

## Moments and samplers

:::exercise{ref=e01}
:::

Every random number your programs use starts as a uniform number. Build the three classic transformations.

:::exercise{ref=e02}
:::

## Bayes' rule

:::exercise{ref=e03}
:::

::::predict{id=p4 kind=numeric answer=0.8 tol=0.05}
The same person takes the test from Section 3 twice, and both results are positive. Assuming the two results are independent given the true state, what is the probability that they have the condition now? Give a decimal.

:::reveal
Apply Bayes' rule twice: the first positive turns the prior $0.01$ into $1/6$, and using $1/6$ as the new prior, the second positive gives $\dfrac{0.99 \cdot 1/6}{0.99 \cdot 1/6 + 0.05 \cdot 5/6} \approx 0.80$. The likelihood ratio of a positive test is $0.99/0.05 \approx 20$; two of them multiply the prior odds by about 400. The independence assumption matters: a repeat of a test that fails for a systematic reason gives far less new information.
:::
::::

## Maximum likelihood

The coin first, with its gradient and its standard error.

:::exercise{ref=e04}
:::

Now the Gaussian, parametrized by $\log\sigma$ so that an optimizer could never produce a negative standard deviation. This trick (optimize an unconstrained quantity, map it to the constrained one) recurs constantly: logits for probabilities, log-variances in normalization, log-scales in quantization.

:::exercise{ref=e05}
:::

The categorical distribution through a softmax. The gradient $N\pi - c$ you derive here is the gradient of every classification loss in this course.

:::exercise{ref=e10}
:::

## Priors and bias

:::exercise{ref=e06}
:::

:::exercise{ref=e07}
:::
