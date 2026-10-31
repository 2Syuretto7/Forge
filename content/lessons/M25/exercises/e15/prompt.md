# Break it: the bootstrap on dependent data

The bootstrap treats the data as independent draws: it resamples single points. A time series with memory is not that, and the bootstrap's error bar comes out far too small. The **block bootstrap** resamples whole stretches instead.

The starter's `ar1(n, rho, rng)` returns a series of length `n` with $x_t = \rho x_{t-1} + \sqrt{1 - \rho^2}\,\varepsilon_t$, whose mean has true standard error about $\sqrt{(1 + \rho)/((1 - \rho)n)}$ (M24, e15).

- `iid_bootstrap_se(x, B, rng)`: the standard deviation of `B` resampled means, resampling single points.
- `block_bootstrap_se(x, block, B, rng)`: build each resample from $\lfloor n/\text{block}\rfloor$ blocks of `block` consecutive points with random starts in `rng.integers(0, n - block + 1, size=(B, n // block))`, and return the standard deviation of the `B` resample means.

The tests show the plain bootstrap's standard error about three times too small at $\rho = 0.8$, and the block bootstrap close to the truth.

## Hints

1. `x[starts[..., None] + np.arange(block)]` has shape `(B, n // block, block)`.
2. Average over the last two axes: `.mean(axis=(1, 2))`.
3. Blocks should be much longer than the memory of the series, about $1/(1 - \rho) = 5$ steps here.
