# Scale and measure: solvers, features and calibration

This movement compares solvers by how many iterations they need, shows how feature engineering lets a linear model draw curved boundaries, and checks calibration on a model that is right about its data.

## Newton's method versus gradient descent

The logistic loss is smooth and convex, and its Hessian is cheap for small $d$. Newton's method uses it to take steps $w \leftarrow w - H^{-1}\nabla L$, which converges quadratically near the optimum: the number of correct digits roughly doubles per iteration.

:::exercise{ref=e12}
:::

::::predict{id=p4 kind=choice answer=a}
For a problem with $d = 10^6$ features (say, a bag of words), why is Newton's method rarely used?

- Each step needs the $d \times d$ Hessian: $10^{12}$ entries to store and about $10^{18}$ operations to factor.
- Newton's method does not converge for convex problems.
- The logistic loss has no Hessian.
- It converges to a worse solution than gradient descent.

:::reveal
Newton's method is superb when $d$ is small and hopeless when $d$ is large: forming and solving with a $d \times d$ matrix costs $O(nd^2 + d^3)$. Large models use first-order methods (L05), sometimes with cheap diagonal or low-rank curvature estimates; Adam's per-parameter scaling is one of them.
:::
::::

## Curved boundaries from linear models

:::exercise{ref=e13}
:::

:::widget{name=DecisionBoundary separable=false lr=0.5 l2=0.01}
:::

With overlapping classes the loss has a finite minimum and the boundary settles. Try raising the L2 strength: the probabilities near the boundary flatten toward $0.5$ and the weight norm shrinks.
