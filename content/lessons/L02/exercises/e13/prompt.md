# Learning curves

How does test error fall as the training set grows? For the sine target and a fixed polynomial degree:

- `learning_curve(sizes, degree, sigma, trials, seed)`: for each training size `n`, average over `trials` the test MSE (against the noise-free target on a fixed grid of 200 points in $[-1, 1]$) of a fit on `n` fresh points drawn from one `np.random.default_rng(seed)` (x then y per trial, sizes in order).

Excess error should fall roughly like $1/n$ once $n$ is well above the number of parameters.

## Hints

1. Test grid: `np.linspace(-1, 1, 200)`.
2. Measuring against the noise-free target isolates bias squared plus variance.
3. For degree $d$ the fit has $d + 1$ parameters; use sizes comfortably above that.
