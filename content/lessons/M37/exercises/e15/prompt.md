# Break it: a model that memorizes

The kernel score of e11 with bandwidth $h = 0$ is the exact score of the training set itself. Sampling with it, run all the way to a tiny $t_{\min}$, reproduces the training points: the generated samples are copies (Section 8). It is the exact minimizer of the empirical score-matching objective, so a flexible enough network trained long enough on few examples heads the same way.

- `kde_score(X, t, centres, h)` as in e11.
- `generate(train, h, n, rng, steps=80, tmin=1e-4)`: reverse sampling in two dimensions with the kernel score.
- `nn_distance(gen, train)`: the median, over generated points, of the distance to the nearest training point.

The tests generate from 30 training points: with $h = 0$ the median distance to the nearest training point is below 0.03, a copy; with $h = 0.2$ it is several times larger, comparable to the distance from fresh data to the training set.

## Hints

1. Compute all pairwise distances with broadcasting: the arrays are small.
2. Fresh samples from the target are a fair yardstick: they are new, not copies.
3. Memorization is a privacy and copyright issue for real image models, and smoothing (or more data) is the defence here too.
