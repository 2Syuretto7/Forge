# Capstone: a scaling law you can bet on

The starter's `make_runs()` returns arrays `N`, `D`, `L` for 48 small training runs, and `held_out()` returns `(N, D, L)` for one run with about 40 times the compute of the largest of them.

1. `fit(N, D, L)`: the five-parameter fit of $L = E + A/N^\alpha + B/D^\beta$ (e09's parametrization and Levenberg-Marquardt), returning `(E, A, alpha, B, beta)`.
2. `bootstrap(N, D, L, B=100, seed=0)`: residual-bootstrap refits, an array of shape `(B, 5)` in the same order.
3. `predict(chin, N, D)` and `predict_interval(samples, N, D, level=0.95)`: the prediction at one point, and the percentile interval of the bootstrap predictions, widened by the residual noise, $\pm 1.96$ times the residual standard deviation added in quadrature to each side's distance from the median.
4. `REPORT`: at least 120 words. Give the fitted exponents with intervals, the predicted loss of the held-out run with its interval and the actual value, the compute-optimal split implied by the fit, and what would make you distrust the prediction.

The tests require both exponents within 0.05 of the generating values, the held-out loss inside your 95 percent interval, and an interval narrower than 0.1.
