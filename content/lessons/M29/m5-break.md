# Break it: plateaus, early steps and too much momentum

## A plateau that is not the optimum

:::exercise{ref=e13}
:::

Turn on gradient noise: SGD stops descending and jitters around the minimum, momentum's jitter is wider, and Adam's per-coordinate normalization amplifies the noise in flat directions. Lower the learning rate and the cloud shrinks.

:::widget{name=LossLandscape surface=quadratic kappa=20 loglr=-1.3 noise=1}
:::

## The first steps of Adam

::::predict{id=p5 kind=choice answer=c}
Adam with $\beta_1 = 0.9$ and $\beta_2 = 0.999$, but without bias correction. How long is its first step, compared with the corrected step $\alpha$?

- About $0.1\alpha$: the first moment starts at 0.
- Exactly $\alpha$.
- About $3.16\alpha$.
- About $10\alpha$.

:::reveal
About $3.16\alpha$: $m_1 = 0.1g$ but $\sqrt{v_1} = \sqrt{0.001}\lvert g\rvert \approx 0.0316\lvert g\rvert$, and the second moment's deficit is the larger. For the first few hundred steps the uncorrected steps stay too long, exactly when the curvature is least known and a large step is most dangerous.
:::
::::

:::exercise{ref=e14}
:::

## Too much momentum

:::exercise{ref=e15}
:::

## What to take away

- A plateau under constant-step SGD is a noise floor until halving the step proves otherwise.
- Keep Adam's bias correction, or warm the step up.
- More momentum is not faster: past the optimum it caps the rate at $\sqrt\beta$.
