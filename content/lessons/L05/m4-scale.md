# Scale and measure: optimizers on the L03 network

The quadratic told us what to expect; now test it on a real network. The exercises in this movement use the L03 digit task and its 64-64-32-10 ReLU network, with the forward and backward pass provided.

:::exercise{ref=e08}
:::

:::exercise{ref=e09}
:::

:::exercise{ref=e10}
:::

::::predict{id=p4 kind=sketch answer="1,0.95,0.85,0.52,0.19,0.06,0.03,0.99" tol=0.2 xlabel="log10 learning rate: -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5" ylabel="final training loss (scaled)"}
Sketch the final training loss after 300 steps of SGD as a function of the learning rate, from $10^{-3}$ to $10^{0.5}$ in half-decade steps.

:::reveal
A slope down to a cliff. At $10^{-3}$ the loss barely moves from its starting value near $\ln 10 \approx 2.3$; it falls steadily as the rate grows and is lowest at a rate of 1 (about 0.06). At $10^{0.5} \approx 3.2$ it is back at 2.3: the first large steps push the second layer's ReLUs into the region where they never fire, and the network can only output the class frequencies. The best rate sits just below the failure point, which is why practical sweeps start high and back off.
:::
::::

:::exercise{ref=e11}
:::
