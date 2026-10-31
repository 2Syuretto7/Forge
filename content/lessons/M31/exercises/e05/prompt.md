# Growth functions and the VC dimension

A class of classifiers that can produce every labelling of $m$ points **shatters** them; the **growth function** $\Pi(m)$ counts the labellings a class can produce on $m$ points, and the **VC dimension** is the largest $m$ it shatters (Section 3). Sauer's lemma bounds the growth function of a class with VC dimension $d$ by $\sum_{i=0}^{d}\binom mi$, a polynomial instead of $2^m$.

- `threshold_labelings(xs)`: the set of labellings (tuples of 0 and 1) of the points `xs` on a line produced by classifiers $1[x \ge \theta]$, over all $\theta$.
- `interval_labelings(xs)`: the same for $1[a \le x \le b]$.
- `sauer_bound(m, d)`.
- `vc_dimension(labelings_fn, max_m=6)`: the largest $m \le$ `max_m` for which the class produces all $2^m$ labellings of the points $0, 1, \dots, m - 1$.

The tests count $m + 1$ labellings for thresholds and $\binom{m + 1}2 + 1$ for intervals, find VC dimensions 1 and 2, and compare with Sauer's bound.

## Hints

1. Thresholds only matter between consecutive sorted points: try $\theta$ below all points, between each pair, and above all.
2. For intervals, try every pair of endpoints chosen from the same candidate positions, plus the empty interval.
3. Represent a labelling as `tuple(int(...) for x in xs)` so that a set removes duplicates.
