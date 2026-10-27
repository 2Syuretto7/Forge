# Nats, bits and perplexity

Implement the unit conversions of Section 7 and the puzzle's interpretation.

- `bits_per_token(nats)`.
- `perplexity(nats)`.
- `nats_from_perplexity(ppl)`.
- `geometric_mean_prob(nats)`: the probability the model assigns to the observed token on average in the geometric-mean sense.
- `uniform_loss(K)`: the loss in nats of a model that is uniform over `K` tokens.

## Hints

1. Divide by $\ln 2$.
2. Perplexity and loss are related by an exponential.
3. The geometric mean of probabilities is $\exp\big(\frac{1}{n}\sum\log p_i\big)$.
