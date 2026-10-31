# Break it: Adam without bias correction

At $t = 1$, $m_1 = (1 - \beta_1)g_1$ and $v_1 = (1 - \beta_2)g_1^2$, both far below the gradient's true moments because they start at zero. Without correction the first step is $\alpha\frac{(1 - \beta_1)}{\sqrt{1 - \beta_2}}$ per coordinate, about $3.16\alpha$ with the defaults: three times the intended size, and in the opposite case ($\beta_1$ large, $\beta_2$ small) far too small (Section 6).

- `first_step(b1, b2, lr=1.0)`: the length of Adam's first step per coordinate, uncorrected, for any nonzero gradient (ignore $\varepsilon$).
- `step_lengths(g, lr, iters, b1=0.9, b2=0.999, bias_correction=True)`: the per-step move of a single coordinate under a constant gradient `g`, as an array.

The tests check the factor $3.16$, the stretch of early steps that are too long without correction, and that the two versions agree after a few thousand steps.

## Hints

1. $\frac{(1 - \beta_1)g}{\sqrt{(1 - \beta_2)g^2}} = \frac{1 - \beta_1}{\sqrt{1 - \beta_2}}$.
2. Reuse the update of e09 on a single scalar.
3. The uncorrected ratio approaches 1 as $\beta_1^t$ and $\beta_2^t$ go to 0: after about $5/(1 - \beta_2) = 5000$ steps.
