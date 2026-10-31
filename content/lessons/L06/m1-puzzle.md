# Puzzle: more layers, worse training

The L03 network had three layers and reached about 90 percent test accuracy. Make it deeper: 20 hidden layers of width 32, He initialization, Adam, everything else the same.

::::predict{id=p1 kind=choice answer=c}
After 300 Adam steps, how does the 20-layer plain network's training loss compare with the 3-layer network's?

- Lower: more layers means more capacity, and Adam handles the rest.
- About the same: the extra layers learn the identity.
- Much higher: the deep network trains worse, although it could represent everything the shallow one does.
- It diverges to infinity.

:::reveal
It trains much worse: in this lesson's experiments the 20-layer plain network ends near a loss of 1.2, while the same depth with residual connections and layer norm reaches about 0.17. A deep network could copy the shallow one by making the extra layers identities, but gradient descent does not find that solution easily. This **degradation problem** is what residual networks (He et al., 2015) were invented to solve.
:::
::::

Watch what happens inside a deep stack in the widget: the scale of the activations from layer to layer, and the scale of the gradients flowing back.

:::widget{name=ActivationStats depth=20 init=he act=relu}
:::

Now turn on the residual connections without normalization. Each layer adds its output to its input.

::::predict{id=p2 kind=numeric answer=1024 tol=150}
Suppose each layer adds a branch whose output is uncorrelated with its input, has zero mean, and has the same second moment as the input. By what factor does the root mean square of the stream grow over 20 layers?

:::reveal
Each layer doubles the second moment, $\mathbb E[(h + F)^2] = \mathbb E[h^2] + \mathbb E[F^2] = 2\,\mathbb E[h^2]$, so after 20 layers it is $2^{20}$ times larger and the RMS is $2^{10} = 1024$ times larger. Residual connections fix the gradient but, unscaled, blow up the forward pass. Normalization or scaled branches fix that, which is the subject of this lesson.
:::
::::
