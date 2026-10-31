# Capstone: an autodiff library for real code

The starter holds `target`, a 20-line function of three variables with arithmetic, powers, a loop, a branch and six elementary functions. Differentiate it two ways: forward mode with dual numbers, one pass per input, and reverse mode with a small graph-recording engine, one backward pass for all three. Both must match a reference to $10^{-9}$ on both sides of the branch, and agree with central differences.

:::exercise{ref=capstone}
:::

## When you finish

You have built the machinery inside every deep-learning framework. L03 uses it to train networks by backpropagation and L04 extends it to tensors; M26 explains why your gradients are exact while finite differences are not; M27 derives the cross-entropy gradient $p - y$ from information theory.

:::edge{to=L03 text="backpropagation through a network, layer by layer."}
:::
