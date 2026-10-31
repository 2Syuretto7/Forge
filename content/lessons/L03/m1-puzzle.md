# Puzzle: what a line cannot do, and a network that cannot start

Three arms of a spiral, one per class, wind around the origin. Logistic regression draws straight boundaries; no arrangement of three lines separates the arms.

::::predict{id=p1 kind=choice answer=b}
You train softmax regression on the three-arm spiral (300 points). What training accuracy do you expect?

- About 100 percent, given enough iterations.
- Around 50 percent: better than chance (33 percent) but far from separating the arms.
- About 33 percent, exactly chance.
- 0 percent, because the classes are interleaved.

:::reveal
A linear classifier carves the plane into three wedges. Each wedge catches part of every arm, so accuracy lands around 50 percent. A network with one hidden layer of 100 ReLU units reaches nearly 100 percent: it builds its own features (bent combinations of the inputs) and then draws linear boundaries in that feature space.
:::
::::

The fix is to learn the features. Stack a layer that computes new features $h = \phi(xW_1 + b_1)$ from the inputs, with a nonlinearity $\phi$ such as ReLU, and feed $h$ into softmax regression. Training adjusts $W_1$ and $b_1$ so that the arms become linearly separable in $h$-space. Computing how to adjust them is backpropagation.

::::predict{id=p2 kind=choice answer=c}
You initialize such a network with every weight and bias equal to zero and train it with gradient descent. What happens?

- It trains normally; initialization only affects speed.
- It trains, but more slowly than with random weights.
- The hidden units stay identical to one another forever, so the network behaves like a model with a single hidden unit.
- The loss is undefined because of division by zero.

:::reveal
With identical weights, every hidden unit computes the same value and receives the same gradient, so after any number of updates they are still identical. (With ReLU and all-zero weights the hidden gradients are even exactly zero.) Random initialization breaks this symmetry. Movement 5 makes you watch it happen.
:::
::::

The widget shows reverse mode on a tiny two-layer network with one input. Step through the backward pass and check each gradient against the chain rule. Then set $w_1 x + b_1$ negative (for instance $w_1 = 1.1$, $x = 0.9$, $b_1 = -2$): the ReLU outputs zero and every gradient upstream of it vanishes. That is a dead unit.

:::widget{name=ComputationGraph preset=mlp}
:::

## Questions to carry into the derivation

1. What exactly does a multi-layer network compute, and why can it represent curved boundaries?
2. What is the backward pass of each layer type, and how do they compose?
3. How much does the backward pass cost compared with the forward pass?
4. Which initializations make training impossible, and why?
