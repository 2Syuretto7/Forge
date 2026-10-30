# A curve that bends without limit

$\sqrt{x}$ near 0 bends harder and harder: its slope is infinite at 0. The $h^2$ law needs bounded bending, so expect it to fail here.

- `sqrt_error(n)`: the largest error of the $n$-piece interpolant of $\sqrt{x}$ on $[0, 1]$, measured with `np.interp` at 20,001 equally spaced points.
- `predicted_sqrt_error(n)`: the exact worst error on the first piece $[0, h]$: the chord is $x / \sqrt{h}$, and the gap $\sqrt{x} - x/\sqrt{h}$ is largest at $x = h/4$, giving $\sqrt{h}/4$ with $h = 1/n$.
- `pieces_for_sqrt(tol)`: the smallest $n$ with `predicted_sqrt_error(n) <= tol`, from the formula (solve for $n$ and round up).

With 30 pieces the hill was within 0.01. How many does $\sqrt{x}$ need on an interval of length 1?

## Hints

1. Set the derivative of $\sqrt{x} - x/\sqrt{h}$ to zero, or just trust the hint and check numerically.
2. $\sqrt{h}/4 \leq \text{tol}$ means $h \leq 16\,\text{tol}^2$, so $n \geq 1/(16\,\text{tol}^2)$.
3. `math.ceil` rounds up; guard against rounding just above a whole number.
