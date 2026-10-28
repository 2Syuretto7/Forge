# Puzzle: ten times the compute

Your lab trained a model for a budget of $C$ FLOPs and the result was good. Next quarter you get $10C$.

::::predict{id=p1 kind=choice answer=c}
To get the lowest loss from $10C$, how should you spend it?

- Keep the token count and make the model 10 times larger.
- Keep the model and train on 10 times as many tokens.
- Grow both: the model and the token count by about 3 times each.
- It does not matter: the loss depends only on the compute.

:::reveal
Loss depends on both the parameter count $N$ and the token count $D$, and compute is roughly $C = 6ND$. Hoffmann et al. (2022) found that the best allocation grows them about equally, $N^* \propto C^{0.5}$ and $D^* \propto C^{0.5}$, so each grows by $\sqrt{10} \approx 3.2$. An earlier study (Kaplan et al., 2020) had concluded that most of the extra compute should go into parameters, $N^* \propto C^{0.73}$. This lesson derives the allocation from a model of the loss, shows how to fit that model to your own runs, and shows how such fits mislead.
:::
::::

The widget plots the loss of models of fixed size trained on more and more tokens (faint curves) against their compute. No single size is best everywhere: each curve is lowest for a while, then flattens as the model runs out of capacity. The lower envelope of all the curves is the compute-optimal frontier.

:::widget{name=ScalingFit}
:::

::::predict{id=p2 kind=choice answer=b}
In the widget, the eight runs between $10^{18}$ and $10^{21}$ FLOPs are fitted with a pure power law $k C^{-\gamma}$ and extrapolated to $10^{24}$, where the true frontier is at 1.91 nats. The prediction is:

- Within 1% of the truth: power laws extrapolate.
- Far too low, around 1.5 nats.
- Far too high, around 2.5 nats.
- Undefined, because the fit diverges.

:::reveal
A pure power law is a straight line in log-log coordinates, but the frontier bends toward an irreducible loss $E$. Fitted on three decades and extended three more, the line keeps falling and predicts about 1.5 nats, roughly 20% below the truth. Switch the fitted form to one with a floor, $E + k C^{-\gamma}$, and the error almost disappears. Section 6 of the derivation and exercise 11 return to this.
:::
::::
