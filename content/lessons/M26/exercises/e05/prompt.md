# Finite differences against the complex step

M15 found that a forward difference $\frac{f(x + h) - f(x)}{h}$ has truncation error proportional to $h$ and rounding error proportional to $\varepsilon/h$, so it is most accurate near $h \approx \sqrt\varepsilon \approx 10^{-8}$, with about 8 correct digits. The **complex step** avoids the subtraction entirely: for real-analytic $f$, $f(x + ih) = f(x) + ihf'(x) - \frac{h^2}{2}f''(x) + \dots$, so

$$
f'(x) \approx \frac{\operatorname{Im} f(x + ih)}{h} ,
$$

with error proportional to $h^2$ and no cancellation, so $h = 10^{-20}$ works.

- `forward_diff(f, x, h)`, `central_diff(f, x, h)` and `complex_step(f, x, h=1e-20)`.
- `error_curve(f, df, x, hs, method)`: the list of absolute errors of `method(f, x, h)` against the exact `df(x)` for each step in `hs`.

The tests run a **gradient check** of each method against an exact derivative, and trace the V-shaped error of the forward difference against the flat floor of the complex step.

## Hints

1. Write `f` with NumPy functions, which accept complex numbers: `np.exp`, `np.sin`, `np.sqrt`.
2. `np.imag(f(x + 1j * h)) / h`.
3. The central difference's best step is near $\varepsilon^{1/3} \approx 6 \times 10^{-6}$.
