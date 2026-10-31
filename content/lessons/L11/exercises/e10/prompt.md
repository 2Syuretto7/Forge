# Running out of data

Data is finite. Muennighoff et al. (2023) model repeated data with diminishing returns: $U$ unique tokens seen for $1 + R$ epochs are worth
$$
D' = U + U R^* \bigl(1 - e^{-R/R^*}\bigr)
$$
fresh tokens, with a fitted constant $R^*$ (about 15 in their fits). `law` is provided.

1. `effective_tokens(unique, epochs, r_star=15.4)`.
2. `loss_with_repeats(N, unique, epochs, E, A, B, alpha, beta, r_star=15.4)`: the parametric loss with $D$ replaced by $D'$.

## Hints

1. $R$ counts repetitions: one epoch means $R = 0$.
2. For small $R$, $1 - e^{-R/R^*} \approx R/R^*$, so a few epochs are worth almost as much as fresh data.
3. As the epochs grow, $D'$ approaches $U(1 + R^*)$: no amount of repetition is worth more than that.
