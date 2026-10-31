# Break it: fast and wrong

::::predict{id=p5 kind=choice answer=c}
A matrix with singular values $1/\sqrt j$, decaying slowly. A rank-10 randomized SVD with no oversampling and no power iterations: how does its spectral-norm error compare with the optimum $\sigma_{11}$?

- Exactly equal.
- About 5 percent larger.
- About twice as large.
- About a hundred times larger.

:::reveal
About twice, varying from run to run between 1.7 and 2.5 in e14. With oversampling 10 and two power iterations it is within half a percent. The Frobenius error looks much better, about 20 percent above optimal, because the long tail it sums is large for every method; the spectral norm shows the largest direction the method missed.
:::
::::

:::exercise{ref=e13}
:::

The singular values of a matrix with a slowly decaying spectrum: the tail beyond any rank you choose is heavy, which is when oversampling and power iterations matter.

:::widget{name=SpectrumBars shape=power noise=0.1 k=10}
:::

:::exercise{ref=e14}
:::

## Accuracy

:::exercise{ref=e15}
:::

## What to take away

- Check a method's assumptions before trusting its output: CG needs a symmetric positive definite matrix.
- Oversample and add a power iteration unless the spectrum is known to decay fast.
- Never form $A^\top A$ for an ill-conditioned least-squares problem.
