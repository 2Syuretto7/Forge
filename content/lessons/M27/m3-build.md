# Build: information measures in code

Eight exercises: the basic quantities, mutual information, the equivalence of maximum likelihood and cross-entropy, units, the two numerically stable losses every classifier uses (M26), and Shannon's bound. Three include gradient checks.

## Entropy, cross-entropy and KL

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

Cross-entropy is entropy plus KL. If training stalls at a loss of $2.1$ nats on data whose entropy is $1.8$ nats, the model is $0.3$ nats from perfect: only that part is reducible, and the remaining $1.8$ nats is the irreducible uncertainty of the data. Scaling-law fits in L11 include exactly this irreducible term.

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
