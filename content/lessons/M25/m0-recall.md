# Recall bridge: from parameters to data and back

M22 and M24 went forward: given a distribution, what do samples look like, and how far does their average stray? Inference goes backward: given the samples, which distribution produced them, and how sure can you be? Every model you train answers this question, usually by maximum likelihood. Clear your due cards above first.

:::edge{from=M24 text="the central limit theorem and confidence intervals"}
:::

:::edge{from=M16 text="maximizing by setting the derivative to zero"}
:::

## What carries over

The sampling distribution of an average, $N(\mu, \sigma^2/n)$, and the interval $\bar x \pm 1.96\,s/\sqrt n$ from M24; Bayes' rule from M21; and from M16, a maximum is where the derivative vanishes and the second derivative is negative.
