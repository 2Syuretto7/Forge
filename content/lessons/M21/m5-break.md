# Break it: counted twice, never seen, and the wrong conditional

## Evidence counted twice

:::exercise{ref=e13}
:::

## A word never seen

::::predict{id=p5 kind=choice answer=d}
Without smoothing, a ham message contains one word that appeared only in spam during training. What does naive Bayes say?

- It mostly ignores the word.
- It lowers the ham probability a little.
- It refuses to classify.
- The ham probability is exactly 0, whatever the other hundred words say.

:::reveal
Exactly 0: the estimated $P(w \mid \text{ham}) = 0$ makes the whole product 0, and in logarithms $-\infty$ overwhelms everything. Laplace smoothing adds a pseudo-count to every word, turning "never seen" into "rare", which can be outvoted.
:::
::::

:::exercise{ref=e14}
:::

## Confusing the conditionals

:::exercise{ref=e15}
:::

:::widget{name=BayesGrid prevalence=1 sensitivity=99 specificity=99.9}
:::

At 99.9 percent specificity the false alarms fall to 1 in 1,000 healthy people, and the posterior rises from 9 to 50 percent: for a rare condition, the false-positive rate matters far more than the sensitivity.

## What to take away

- Ask for the base rate before interpreting any test.
- Smooth counts; a zero probability is a claim of impossibility.
- Treat naive Bayes probabilities as scores until calibrated.
