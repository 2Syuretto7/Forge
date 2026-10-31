# Break it: a factor of two, fifty times

Initialize a 50-layer ReLU network with weight variance $c\cdot\frac2{n_{\text{in}}}$. Each layer multiplies the second moment of the activations by $c$ (e06), so after 50 layers it has been multiplied by $c^{50}$ (Section 5). With $c = \frac12$, Xavier's variance used with ReLUs, that is $2^{-50} \approx 10^{-15}$; with $c = 2$, about $10^{15}$.

- `forward_second_moments(L, width, c, rng, batch=64)`: push a batch of standard normal inputs through $L$ layers of width `width`, each a matrix product followed by a ReLU, with fresh weights of variance $2c/\text{width}$; return the list of the activations' mean squares after each layer.
- `predicted_ratio(c, L)`: $c^L$.

The tests find He initialization ($c = 1$) holding the second moment within a factor of 5 over 50 layers, and the measured ratios for $c = \frac12$ and $c = 2$ within a factor of 30 of $c^{50}$, about 15 orders of magnitude away from 1.

## Hints

1. Divide by the input's second moment to get a ratio; the first ReLU halves a standard normal's.
2. Compare in log space: `abs(log10(measured) - log10(predicted))`.
3. Normalization layers, residual connections and careful initialization all exist to keep this product near 1.
