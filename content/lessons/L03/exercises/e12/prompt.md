# Break it: exploding activations

Push a batch through a deep stack of ReLU layers (no training) and watch its scale.

- `activation_rms(depth, width, std, seed, batch)`: draw `batch` standard-normal inputs of dimension `width` and `depth` weight matrices of shape `(width, width)` with entries $\mathcal N(0, \text{std}^2)$, all from one `np.random.default_rng(seed)` (inputs first). Apply $h \leftarrow \operatorname{ReLU}(hW)$ for each layer. Return the list of RMS values $\sqrt{\text{mean}(h^2)}$ after each layer.
- `predicted_growth(width, std)`: Section 7's per-layer factor $\text{std}\sqrt{\text{width}/2}$.

## Hints

1. `rms = np.sqrt(np.mean(h ** 2))`.
2. With `std = 1` and `width = 256` the RMS grows by about 11 per layer.
3. With He's `std = sqrt(2 / width)` it stays near its starting value.
