# Break it: too fast, uncorrected, and decayed the wrong way

## A learning rate that is too high

Gradient descent diverges once $\eta$ passes $2/\lambda_{\max}$, and a neural network is no different: its loss either explodes to infinity or, with ReLUs, kills most units on the first big step and stalls. In the `LossLandscape` widget, set the learning rate just above the stability limit and watch the steep direction grow. Exercise 2 measured that limit; exercise 11 found the network's.

::::predict{id=p5 kind=choice answer=a}
You train with Adam and remove the bias correction, keeping $\beta_1 = 0.9$ and $\beta_2 = 0.999$. What happens to the first hundred steps?

- They are about 3 to 6.5 times larger than intended.
- They are about 10 times smaller, because $m$ starts at zero.
- They are unchanged, because the two biases cancel.
- Only the first step is affected.

:::reveal
Without correction, the step is $\hat m/\sqrt{\hat v}$ times $(1 - \beta_1^t)/\sqrt{1 - \beta_2^t}$. At $t = 1$ that factor is $0.1/\sqrt{0.001} \approx 3.16$; it peaks near $6.6$ around step 12, and is still above 3 at step 100, because $\beta_2^t$ takes about a thousand steps to fade. The bias in $v$ is the stronger one, and it makes early steps too large, exactly when training is most fragile.
:::
::::

:::exercise{ref=e12}
:::

## Weight decay inside Adam

:::exercise{ref=e13}
:::

## What to take away

- The largest stable learning rate is set by the steepest direction; find it, then back off.
- Keep Adam's bias correction, or compensate with a long warmup.
- Use decoupled weight decay (AdamW) with adaptive optimizers; L2 inside Adam decays each weight at a rate set by its gradient history.
