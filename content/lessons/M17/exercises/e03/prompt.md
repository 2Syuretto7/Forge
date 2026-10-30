# Adaptive Simpson

`adaptive_simpson(f, a, b, tol=1e-10, max_depth=50)`: return `(value, evaluations)`.

On an interval, compute Simpson's rule $S$ with its midpoint, and $S_2$ as the sum of Simpson's rule on the two halves. If $|S_2 - S| \leq 15\,\text{tol}$, accept $S_2 + (S_2 - S)/15$ (the difference estimates the error, and the correction is Richardson's, M17 e11); otherwise recurse on both halves with `tol / 2`. Reuse function values: each refinement costs two new evaluations. Count every call to `f`.

The tests compare with a fixed Simpson rule on $1/(x + 0.001)$, whose difficulty sits near 0: adaptivity needs about a hundred times fewer evaluations for the same accuracy. They also show adaptivity fooled: a peak narrower than the first five sample points is invisible to it, and it stops after five evaluations with a confident, wrong answer.

## Hints

1. A recursive helper takes the end points, the three known values and the whole-interval estimate.
2. Wrap `f` in a counter: a list with one integer, incremented in a small function.
3. Python's default recursion limit is 1,000; `max_depth` keeps you far from it.
