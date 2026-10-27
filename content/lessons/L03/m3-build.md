# Build: differentiation tools

You will build the instruments you need to trust every gradient in this course, then the Jacobians that every network is made of. Four exercises include gradient checks.

## Finite differences and a gradient checker

:::exercise{ref=e01}
:::

:::exercise{ref=e03}
:::

:::exercise{ref=e04}
:::

## Forward mode with dual numbers

Dual numbers give exact derivatives with no step size at all. You will reuse this class in the capstone.

:::exercise{ref=e05}
:::

## JVPs, VJPs and the Jacobians of common layers

The next exercise makes the two products of Section 4 concrete for one layer. Notice that neither product needs the Jacobian matrix.

:::exercise{ref=e06}
:::

::::predict{id=p3 kind=numeric answer=50000 tol=5000}
A language model's output layer applies a softmax over a vocabulary of 50,000 tokens. The full softmax Jacobian has $50{,}000^2 = 2.5 \times 10^9$ entries. How many multiply-adds (to the nearest few thousand) does the VJP $p \odot (u - u^\top p)$ need?

:::reveal
The dot product $u^\top p$ costs $K = 50{,}000$ multiply-adds, then the elementwise product another $K$, so about $10^5$ operations, of order $K$ rather than $K^2$. Reverse mode never needs a full Jacobian: every layer only needs to apply its transpose to a vector.
:::
::::

:::exercise{ref=e07}
:::

:::exercise{ref=e08}
:::

:::exercise{ref=e09}
:::

:::widget{name=ComputationGraph preset=neuron}
:::

Use the widget to watch reverse mode on a single neuron with a squared loss. Check by hand that the gradient arriving at $z$ equals $2(s - t)\, s(1 - s)$, the product of the two local derivatives above it.
