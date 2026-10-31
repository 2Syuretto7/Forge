# Capstone: a Gaussian toolkit and a tracker

Build sampling, a stable log-density and conditioning for Gaussian vectors, then a Kalman filter that follows a target moving at nearly constant velocity from noisy position readings. The filter must cut the root-mean-square position error of the raw measurements by more than half, using nothing but Gaussian conditioning and the dynamics.

:::exercise{ref=capstone}
:::

## When you finish

You can describe uncertainty in many dimensions, read its shape, sample it, and update it with evidence. M24 studies averages of many samples and their bell curves; M37 runs Gaussian noise forward and learns to run it backwards.

:::edge{to=M37 text="stochastic differential equations and diffusion."}
:::
