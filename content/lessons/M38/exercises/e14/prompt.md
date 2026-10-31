# Adam, break it: no bias correction

Remove the bias corrections from e11 (Section 5). At $t = 1$, $m_1 = (1 - \beta_1)g$ and $v_1 = (1 - \beta_2)g^2$, so the update is

$$
\eta\,\frac{(1 - \beta_1)}{\sqrt{1 - \beta_2}}\,\mathrm{sign}(g) \approx 3.16\,\eta\,\mathrm{sign}(g)
$$

for the default $\beta_1 = 0.9$, $\beta_2 = 0.999$: more than three times the intended step, and it stays too large for hundreds of steps while $v$ warms up more slowly than $m$.

- `uncorrected_step_sizes(g, steps, lr=1.0, b1=0.9, b2=0.999)`: the update sizes $\lvert\Delta x\rvert$ for a constant scalar gradient `g`, without corrections.
- `corrected_step_sizes(g, steps, lr=1.0, b1=0.9, b2=0.999)`: the same with corrections, all equal to `lr`.
- `peak_ratio(b1, b2, steps=2000)`: the largest uncorrected step divided by the corrected one.

The tests find the first uncorrected step $3.16$ times too large, steps above twice the intended size for more than 50 steps, and convergence to the intended size only after thousands of steps.

## Hints

1. For a constant gradient, $m_t = (1 - \beta_1^t)g$ and $v_t = (1 - \beta_2^t)g^2$.
2. The uncorrected ratio is $(1 - \beta_1^t)/\sqrt{1 - \beta_2^t}$; differentiate or tabulate it.
3. Learning-rate warm-up, used with Adam almost everywhere, also tames these early steps.
