# Counting mini-batches

- `log10_comb(n, k)`: $\log_{10} \binom{n}{k}$ from the log-gamma function, $\ln \Gamma(m + 1) = \ln m!$, without computing the binomial coefficient: `math.lgamma`.
- `digits_of_comb(n, k)`: the number of decimal digits of $\binom{n}{k}$, from `log10_comb` (floor plus one).
- `steps_per_epoch(n, batch)`: the number of mini-batches needed to see each of `n` examples once, with a final partial batch.
- `epochs_before_repeat_is_likely(n, batch)`: if every epoch draws its mini-batches at random, how many mini-batches can be drawn before some exact batch is likely (probability one half) to have appeared twice? Use the birthday bound: about $\sqrt{2 \ln 2 \cdot N}$ draws for $N$ possible batches, so return its base-10 logarithm, $\frac{1}{2}\log_{10}(2 \ln 2) + \frac{1}{2}\log_{10} N$.

## Hints

1. `(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)) / math.log(10)`.
2. Compare with `len(str(math.comb(n, k)))` for moderate sizes.
3. `math.ceil(n / batch)`.
