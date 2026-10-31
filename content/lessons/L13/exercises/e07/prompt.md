# Stochastic rounding

On a grid of spacing `step`:

1. `round_down_up(x, step)`: the grid points just below and just above `x`.
2. `stochastic_round(x, step, rng)`: round `x` up with probability $(x - \ell)/\text{step}$, where $\ell$ is the point below, and down otherwise.
3. `accumulate(w0, update, n, step, mode, rng=None)`: apply $w \leftarrow \operatorname{round}(w + \text{update})$ `n` times, with `mode` `"nearest"` or `"stochastic"`.

Start from 1.0 on bf16's grid near 1 ($2^{-7}$) and add 0.001 a thousand times.

## Hints

1. `lo = np.floor(x / step) * step`.
2. `rng.random(shape) < p` picks "up" with probability `p`.
3. The expected value of a stochastic rounding is exactly `x`.
