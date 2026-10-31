# Capstone: a hand-differentiated MLP on digits

Put everything together: a two-hidden-layer network, your own backward pass, minibatch training, and an honest test score. The dataset is a set of 8 by 8 images of digit-like glyphs, shifted, faded, with missing pixels and noise. A linear classifier manages about 73 percent; a well-trained MLP clears 88.

:::exercise{ref=capstone}
:::

## When you finish

Writing backward passes by hand teaches exactly what each gradient is, and it does not scale: every new layer type means new derivations and new bugs. L04 builds an autograd engine that records operations during the forward pass and runs their VJPs automatically; you will retrain this same network with it and compare the gradients against yours.

:::edge{to=L04 text="Retrain this network with an autograd engine and compare every gradient."}
:::

:::edge{to=L09 text="The same backward pass, extended to attention and residual blocks."}
:::
