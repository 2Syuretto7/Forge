# Scale: 20,000 points, a thousand dimensions, 500 eigenvalues

::::predict{id=p4 kind=choice answer=c}
Project 20,000 points from 128 dimensions to 16 with a Gaussian matrix. By how much does a typical squared distance change?

- By about 3 percent.
- By about 10 percent.
- By about 35 percent.
- By about 100 percent.

:::reveal
About 35 percent: the ratio is $\chi^2_{16}/16$, with standard deviation $\sqrt{2/16} \approx 0.35$. Projection to very few dimensions keeps distances only on average; the lemma's guarantee for every pair needs $k$ in the hundreds or thousands, and the spread shrinks only like $1/\sqrt k$.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

Plant a direction and raise its strength $\ell$ past $\sqrt\gamma$: the top eigenvalue leaves the bulk exactly where the BBP formula says.

:::widget{name=RandomSpectrum p=120 gamma=0.25 spike=1}
:::

:::exercise{ref=e12}
:::
