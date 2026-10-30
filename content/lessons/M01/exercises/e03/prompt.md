# Significant figures and the error of an estimate

- `round_sig(x, n)` rounds `x` to `n` significant figures: `round_sig(123456, 2)` is `120000`, `round_sig(0.0012345, 3)` is `0.00123`. Zero stays zero.
- `relative_error(estimate, truth)` is `abs(estimate - truth) / abs(truth)`.
- `factor_off(estimate, truth)` is `max(estimate / truth, truth / estimate)` for positive numbers. It is 1 for a perfect estimate, 2 for one twice too big or half as big. Raise a `ValueError` if either number is not positive, with `raise ValueError("...")`.

Python's built-in `round(x, k)` rounds to `k` decimal places, and `k` may be negative: `round(123456, -4)` is `120000`. The number of decimal places that keeps `n` significant figures is `n - 1 - floor(log10(abs(x)))`.

## Hints

1. For `x = 123456`, `floor(log10(x))` is 5, so keep `2 - 1 - 5 = -4` decimals.
2. `if estimate <= 0 or truth <= 0: raise ValueError("factor_off needs positive numbers")`.
3. `max(a, b)` returns the larger of two numbers.
