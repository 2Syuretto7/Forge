# Capstone: a gradient-check harness

The starter holds 25 vector functions with hand-written Jacobians, from elementwise activations to softmax, layer normalization and coordinate changes. Some of the Jacobians are wrong. Build a harness that checks each one at several random points with central differences, scaled steps and a relative error, reports every function whose Jacobian disagrees by more than $10^{-6}$, and passes every correct one.

:::exercise{ref=capstone}
:::

## When you finish

You can derive a Jacobian and prove it right. M19 makes the derivation automatic: a program that records the operations of a function computes its exact gradient for about the cost of two evaluations. M20 uses the Jacobian's determinant to transform probability densities, and M28 uses the Hessian to define convexity in many dimensions.

:::edge{to=M19 text="automatic differentiation: exact gradients at the cost of about two evaluations."}
:::
