# Capstone: when two ways of being careful disagree

Real decisions about products, models and experiments are made from small, noisy samples. The two standard tools for quantifying uncertainty, resampling and Bayesian posteriors, usually agree. The interesting cases are where they do not, and the capstone has you find and explain them.

You will need: the bootstrap from exercise 9, the Beta posterior from exercise 6, and the Monte Carlo comparison from exercise 13.

:::exercise{ref=capstone}
:::

## When you finish

The same reasoning returns three times later in the course:

- L06 uses held-out data and cross-validation, which are resampling ideas applied to model selection.
- L21 trains a reward model with a Bradley-Terry likelihood: maximum likelihood on pairwise preferences.
- L23 builds an evaluation harness whose headline numbers come with bootstrap intervals, and asks the same question you asked here: is model B really better than model A?

:::edge{to=L23 text="Is model B really better than model A? The same question, asked of benchmark scores."}
:::
