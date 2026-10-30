# The bounds that make the shift safe

Section 4 showed $\max z \leq \operatorname{LSE}(z) \leq \max z + \ln n$. Check it, and check that the shift is exact.

- `lse(z)`: log-sum-exp of a NumPy array with the max shift.
- `lse_shifted(z, c)`: $c + \ln \sum e^{z_j - c}$ for any shift `c` (not only the maximum).
- `bounds_hold(z)`: whether $\max z \leq \operatorname{LSE}(z) \leq \max z + \ln n$ (allow `1e-12` slack).
- `shift_is_exact(z, cs)`: whether `lse_shifted(z, c)` agrees with `lse(z)` to `1e-9` for every shift in `cs` that does not overflow (skip any `c` for which `np.exp(z - c)` overflows or underflows to all zeros).

The tests try many random vectors, and shifts from far below to far above the scores.

## Hints

1. `m = z.max(); return m + np.log(np.exp(z - m).sum())`.
2. With `np.errstate(all="ignore")`, compute `s = np.exp(z - c).sum()` and skip unless `0 < s < inf`.
3. The upper bound is reached when all scores are equal.
