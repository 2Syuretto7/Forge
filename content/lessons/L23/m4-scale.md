# Scale it: finding features and the components that matter

:::exercise{ref=e08}
:::

::::predict{id=p3 kind=choice answer=c}
A two-layer attention-only transformer is trained on sequences made of a random block of tokens followed by the same block again. How does its loss on the second copy compare with the first?

- About the same: the tokens are random, so nothing is predictable.
- Somewhat lower, from learning which tokens are common.
- Far lower, close to zero once training has gone on long enough: an induction circuit looks up each token's earlier occurrence and copies what followed it.
- Higher, because the model has to remember the first copy.

:::reveal
The first copy is random, so its loss stays near $\ln V$ for a vocabulary of $V$ tokens. The second copy is fully predictable from the first, and the network learns a previous-token head and an induction head that together look up and copy. The drop is abrupt during training. The capstone trains exactly this model and locates the two heads.
:::
::::

:::exercise{ref=e09}
:::

:::exercise{ref=e10}
:::
