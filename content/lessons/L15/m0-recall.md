# Recall bridge: capacity, learning rates and the loss

From L06: test error depends on capacity and on how much data the model sees, and the bias-variance picture changes once models are large enough to interpolate. From L09: the learning rate and its schedule decide how far a training run gets; a rate tuned for one model is not right for another. From L14: a language model's validation loss in nats per token is the number everyone reports. This lesson asks how that number falls as you spend more parameters, more tokens and more compute, and how to spend a budget well. Reviews due from L06, L09 and L14 appear above.

::::derivation{id=d0 title="Warm-up: lines in log-log coordinates"}
:::step
For $y = 5 x^{-0.5}$, at $x = 100$ the value is $y =$ [[0.5]].
:::
:::step
Taking logarithms, $\log y = \log 5 - 0.5 \log x$: a straight line in $(\log x, \log y)$ with slope [[-0.5]].
:::
:::step
Multiplying $x$ by 10 multiplies $y$ by $10^{-0.5} \approx$ [[0.3162|tol=0.0005]], whatever $x$ was.
:::
::::
