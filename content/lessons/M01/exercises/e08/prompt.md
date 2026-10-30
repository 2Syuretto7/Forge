# A Fermi worksheet

A worksheet is a list of factors, each `(lo, hi, op)` where `op` is `"*"` to multiply or `"/"` to divide. The estimate starts from 1.

- `fermi(factors)` returns the interval `(lo, hi)` of the result: multiply by `[lo, hi]` or divide by it, exactly as in the previous exercise.
- `central(factors)` returns the geometric midpoint of that interval.
- `worst_factor(factors)` returns the factor that the interval spans either side of its midpoint: $\sqrt{\text{hi}/\text{lo}}$ of the result.
- `typical_factor(factors)` returns the typical error of Section 5: with each factor's half-width $h_i = \log_{10} \sqrt{\text{hi}_i/\text{lo}_i}$, it is $10^{\sqrt{h_1^2 + h_2^2 + \dots}}$.

## Hints

1. Dividing by `[lo, hi]` divides the running low by `hi` and the running high by `lo`.
2. `worst_factor` equals $10^{h_1 + h_2 + \dots}$; check that your two ways of computing it agree.
3. `math.log10`, `math.sqrt` and `sum` are all you need for `typical_factor`.
