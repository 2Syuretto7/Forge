# Checking a sampler with a histogram

- `histogram_density(samples, bins, lo, hi)`: `(centers, density)`: counts in `bins` equal bins of $[lo, hi]$ divided by (number of samples times bin width), so that it estimates the density.
- `max_relative_deviation(samples, pdf, bins, lo, hi, min_expected=1000)`: the largest $|\text{observed} - \text{expected}| / \text{expected}$ over bins whose expected count, `len(samples)` times `pdf(center)` times the width, is at least `min_expected`.

A correct sampler of 200,000 points gives a few percent; a wrong density, far more.

## Hints

1. `np.histogram(samples, bins=bins, range=(lo, hi))`.
2. Counts outside $[lo, hi]$ are simply not counted.
3. Skip bins with small expected counts: a bin expecting $N$ samples fluctuates by about $\sqrt N$, so 100 expected samples already mean 10 percent noise.
