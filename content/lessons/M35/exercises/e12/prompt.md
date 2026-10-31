# Measuring extrapolation error

Do the delta-method bands of e08 tell the truth beyond the data? Simulate it (Section 5): draw many datasets from a known law on $x \in [1, 100]$, fit each, predict at $10^3$ and $10^4$, and compare the actual errors with the bands.

- `model`, `jacobian` and `fit` as in e06.
- `extrapolation_trial(x, theta_true, sigma, x0s, rng)`: one simulated dataset; return the prediction errors $\hat L(x_0) - L(x_0)$ and the delta-method standard errors, as two arrays over `x0s`.
- `coverage(errors, ses, z=1.96)`: the fraction of trials with $\lvert\text{error}\rvert \le z\cdot\text{se}$, per column.
- `rms_error(errors)`: per column.

The tests run 200 trials and find the root-mean-square error growing with distance, and the 95 percent band covering between 88 and 99 percent of the time: when the model's form is right, extrapolation is uncertain but honest.

## Hints

1. Fit from a start near the truth to avoid wasting iterations; the bootstrap of e07 is the slower but assumption-free alternative.
2. Stack the per-trial arrays with `np.array(list_of_arrays)`.
3. Everything here assumes the model's form is right beyond the data. e14 removes that assumption.
