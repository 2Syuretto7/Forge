# Scale: PageRank on 100,000 pages

A dense $100{,}000 \times 100{,}000$ matrix needs 80 GB. A web graph with ten links per page has a million nonzero entries: about 16 MB as two index arrays. Power iteration only ever needs the product $Px$, which a sparse representation computes in $O(\text{links})$ time.

::::predict{id=p4 kind=numeric answer=113 tol=5}
With damping $d = 0.85$, the error of PageRank's power iteration shrinks by at most $0.85$ per step. How many steps guarantee an error below $10^{-8}$?

:::reveal
$\ln(10^{-8}) / \ln(0.85) \approx 113$. Real web graphs have many closed groups of pages, so $|\lambda_2|$ is exactly $d$ and the bound is reached; a random, well-connected graph mixes faster. The number of steps does not depend on the number of pages, which is why PageRank scaled to billions.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::

The widget's Markov chain has eigenvalues 1 and 0.4. Raise $k$ and watch the angle to the stationary direction shrink by a factor of 0.4 per step.

:::widget{name=EigenFlow preset=markov steps=5}
:::
