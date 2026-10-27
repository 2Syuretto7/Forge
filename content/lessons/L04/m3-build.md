# Build: information measures in code

Eight exercises: the basic quantities, mutual information, the equivalence of maximum likelihood and cross-entropy, units, and the two numerically stable losses every classifier uses. Three exercises include gradient checks.

## Entropy, cross-entropy and KL

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

::::predict{id=p3 kind=choice answer=b}
You fit a model $q$ to data from $p$ by minimizing cross-entropy, and training stalls at a loss of $2.1$ nats. Someone tells you the true entropy of the data is $1.8$ nats. What is $\mathrm{KL}(p\|q)$ at the end of training?

- $3.9$ nats
- $0.3$ nats
- $-0.3$ nats
- It cannot be determined from these numbers.

:::reveal
Cross-entropy equals entropy plus KL, so $\mathrm{KL} = 2.1 - 1.8 = 0.3$ nats. Only that part of the loss is reducible; the remaining $1.8$ nats is the irreducible uncertainty of the data. Scaling-law fits in L15 include exactly this irreducible term.
:::
::::

:::exercise{ref=e04}
:::

## Maximum likelihood is minimum cross-entropy

:::exercise{ref=e05}
:::

:::exercise{ref=e06}
:::

## Stable losses from logits

These two functions are, line for line, the losses inside every classifier and language model you will train.

:::exercise{ref=e07}
:::

:::exercise{ref=e12}
:::

## Codes

:::exercise{ref=e13}
:::
