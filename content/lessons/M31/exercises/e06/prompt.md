# The bias-variance decomposition, by repeated sampling

For squared loss, the expected error of a learned predictor $\hat f$ at a point $x$, averaged over training sets and noise, splits exactly (Section 4):

$$
\mathbb{E}\big[(y - \hat f(x))^2\big] = \underbrace{\sigma^2}_{\text{noise}} + \underbrace{(\mathbb{E}\hat f(x) - f(x))^2}_{\text{bias}^2} + \underbrace{\operatorname{Var}\hat f(x)}_{\text{variance}} .
$$

Fit polynomials of degree `deg` to $n = 20$ noisy samples of $f(x) = \sin(2\pi x)$ on $[0, 1]$ with noise $\sigma = 0.3$.

- `fit_predict(x_train, y_train, deg, x_test)`: least-squares polynomial fit (`np.polyfit`), evaluated at `x_test`.
- `decompose(deg, datasets, rng, x_test)`: draw `datasets` training sets (inputs uniform, from `rng`), fit each, and return a dict with `"bias2"`, `"variance"` and `"noise"` averaged over `x_test`, and `"test_mse"`, the average squared error on fresh noisy targets at `x_test`.

The tests check that the three parts add up to the measured test error, that bias falls from degree 1 to 5 while variance rises from degree 3 to 9, and that the cubic beats both extremes. (A straight line is not the least variable fit here: its misfit makes it sensitive to where the 20 points happen to fall.)

## Hints

1. Stack the predictions of all datasets into a `(datasets, len(x_test))` array; its column means estimate $\mathbb{E}\hat f$.
2. Draw the fresh targets for `test_mse` from the same noise.
3. The identity holds exactly in expectation; with a few hundred datasets the measured sum agrees to a few percent.
