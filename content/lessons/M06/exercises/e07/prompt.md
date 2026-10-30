# Softmax

- `softmax_naive(z)`: for a list of scores, $e^{z_i} / \sum_j e^{z_j}$, exactly as written.
- `softmax(z)`: the same after subtracting $\max z$ from every score (Section 4).
- `argmax(z)`: the index of the largest score (the first one on ties).

The tests check that the outputs are positive and sum to 1, that adding a constant to every score changes nothing, that the order of the probabilities follows the order of the scores, and that `softmax` survives scores of 1000.

## Hints

1. `m = max(z)`, then `es = [math.exp(v - m) for v in z]`.
2. Divide each by `sum(es)`.
3. `z.index(max(z))`.
