# Recall bridge: a gradient is a product of Jacobians

M18 wrote the derivative of a composition as a product of Jacobians and checked gradients with finite differences, at $2n$ evaluations for $n$ inputs. A network with $10^8$ parameters makes that hopeless. This lesson computes the same product in an order that costs a few evaluations, whatever $n$ is: the idea behind every deep-learning framework. Clear your due cards above first.

:::edge{from=M18 text="Jacobians and the chain rule as their product"}
:::

:::edge{from=M27 text="the cross-entropy gradient through a softmax, read across the probability strand"}
:::

## What carries over

Matrix products are associative (M10): $(AB)C = A(BC)$. The result does not depend on the order; the cost does, enormously.
