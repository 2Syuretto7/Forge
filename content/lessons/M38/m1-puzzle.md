# Puzzle: what will the paper need?

Before reading a paper's method section, predict which mathematics it will lean on. A good prediction tells you where to slow down.

::::predict{id=p1 kind=choice answer=a}
DPO trains a language model directly on preference pairs, with no reward model. Which lesson does its central derivation lean on most?

- M30: the optimum of a KL-regularized objective has the Gibbs form.
- M33: randomized linear algebra.
- M37: stochastic differential equations.
- M14: the singular value decomposition.

:::reveal
M30. The paper's first step is that $\max_\pi\mathbb{E}_\pi[r] - \beta\,\mathrm{KL}(\pi\,\|\,\pi_{\text{ref}})$ is solved by $\pi^* \propto \pi_{\text{ref}}e^{r/\beta}$, the Gibbs form you derived from a Lagrangian. Everything else follows by inverting it.
:::
::::

::::predict{id=p2 kind=numeric answer=0.39 tol=0.05}
LoRA adds a rank-8 update $BA$ to a $4096 \times 4096$ weight matrix and trains only $A$ and $B$. What percentage of the matrix's parameters does it train?

:::reveal
About $0.39$ percent: $8 \times (4096 + 4096) = 65{,}536$ parameters against $16{,}777{,}216$. The optimizer state shrinks by the same factor, which is most of LoRA's memory saving.
:::
::::

Every paper's mathematics is a computation graph: each equation a node, each step an edge from an earlier result. Trace one.

:::widget{name=ComputationGraph preset=default}
:::

## Questions to carry into the derivation

1. Which assumptions does each paper make, stated or not?
2. Where does each equation come from, step by step?
3. What small experiment would confirm the central claim?
4. Which assumption, removed, breaks the claim?
