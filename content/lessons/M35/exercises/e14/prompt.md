# Break it: the law changes beyond the data

Every band so far assumed the model's form holds where there are no data. Suppose instead the true curve bends: a **broken power law** whose exponent drops from $0.5$ to $0.2$ beyond $x_b = 10^3$, a regime the data never reached (Section 7). The fit is excellent, the bands are narrow, and the truth falls outside them.

- `broken_law(x, E=1.7, A=2.0, a1=0.5, a2=0.2, xb=1e3)`: $E + Ax^{-a_1}$ for $x \le x_b$, and $E + Ax_b^{-a_1}(x/x_b)^{-a_2}$ beyond, continuous at $x_b$.
- `fit_and_band(x, y, x0, z=1.96)`: fit $E + Ax^{-\alpha}$ (Levenberg-Marquardt) and return the prediction and its delta-method half-width at `x0`.
- `inside(pred, half, truth)`: whether the truth is in the band.

The tests fit 30 points on $[1, 100]$ from the broken law and find the band containing the truth at $x_0 = 500$ and missing it at $x_0 = 10^5$.

## Hints

1. Below $x_b$ the broken law is exactly e04's model, so nothing in the data hints at the break.
2. The band measures noise in the parameters, not doubt about the model.
3. The defence is not statistics but evidence: a run at the target scale, or at least a few runs much closer to it.
