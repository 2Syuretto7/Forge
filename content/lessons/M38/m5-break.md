# Break it: one assumption each

::::predict{id=p5 kind=choice answer=c}
Reddi, Kale and Kumar's online problem: losses $3x$ every third step and $-x$ otherwise, on $[-1, 1]$, whose average is minimized at $x = -1$. Where does Adam with $\beta_1 = 0$ and $\beta_2 = 0.1$ end up?

- At $-1$, the minimum.
- At 0.
- At $+1$, the maximum of the average loss.
- It keeps oscillating across the whole interval.

:::reveal
At $+1$. The rare large gradient inflates $v$, which then decays before the next one; the frequent small gradients are divided by a small $\sqrt v$ and win. AMSGrad, dividing by the running maximum, lands at $-1$. e15 reproduces both.
:::
::::

:::exercise{ref=e05}
:::

:::exercise{ref=e10}
:::

The graph of a computation shows where each assumption enters: follow the edges from the loss back to the step that needs it.

:::widget{name=ComputationGraph preset=default}
:::

:::exercise{ref=e14}
:::

:::exercise{ref=e15}
:::

## What to take away

- State every assumption a derivation uses, especially the ones the paper does not.
- Reproduce on a problem with a known answer before trusting the method on one without.
- Break one assumption deliberately: the failure should be the one the derivation predicts.
