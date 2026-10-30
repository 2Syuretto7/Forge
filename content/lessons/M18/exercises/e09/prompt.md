# Contours cross gradients at right angles

- `contour_segments(f, level, box, n)`: marching squares on an `n` by `n` grid over $[-\text{box}, \text{box}]^2$: in each cell, find the edges where $f - \text{level}$ changes sign, place a point on each by linear interpolation, and join the first two into a segment (and the next two, if there are four). Return a list of `(p, q)` pairs of 2-D points.
- `max_cosine(segments, grad)`: the largest $|\cos|$ of the angle between a segment's direction and the gradient at its midpoint, over all segments with nonzero gradient.

On a fine grid the gradient is perpendicular to every contour piece: `max_cosine` is small.

## Hints

1. Corners in order: bottom-left, bottom-right, top-right, top-left; edges between consecutive corners.
2. The crossing on an edge from value $a$ to value $b$ is at fraction $a/(a - b)$.
3. The cosine is $\frac{|d \cdot g|}{\|d\|\,\|g\|}$.
