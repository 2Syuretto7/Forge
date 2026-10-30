# Puzzle: a million inputs, one output

A loss $L(w)$ depends on a million parameters. You want its gradient.

::::predict{id=p1 kind=numeric answer=2000000 tol=1}
How many evaluations of $L$ do central differences need for the full gradient?

:::reveal
Two million: two per parameter. At a millisecond each, half an hour for one gradient, and training needs millions of gradients. Finite differences are a way to test gradients, not to compute them.
:::
::::

::::predict{id=p2 kind=choice answer=c}
Reverse-mode automatic differentiation, which every framework uses, computes the same gradient exactly. About how much does it cost?

- A million times the cost of $L$, like forward differences.
- About a thousand times the cost of $L$, the square root.
- A small constant times the cost of $L$, typically 2 to 4, whatever the number of parameters.
- Nothing extra: gradients come for free.

:::reveal
A small constant times one evaluation. Reverse mode runs the computation forward once, storing intermediate values, then sweeps backward once, at each operation multiplying an incoming row vector by that operation's local derivatives. One sweep produces all million partial derivatives. The price is memory: the stored intermediates.
:::
::::

The graph computes $f = (xy + \sin x)^2$. The forward pass fills in values; the backward pass sends gradients from $f$ back to the inputs. Notice where $x$ is used twice.

:::widget{name=ComputationGraph preset=default}
:::

## Questions to carry into the derivation

1. How do you differentiate an expression with matrices in it?
2. What are the two cheap products a Jacobian supports without being formed?
3. Why does sweeping backwards give every partial derivative at once?
4. What must happen when a value feeds into two later operations?
