# Explain it plainly: why Adam and warmup

Explain to a programmer who has trained a model with plain SGD why practitioners usually use Adam with warmup and a decaying schedule.

- Write 150 to 400 words.
- Use the picture of a long narrow valley.
- Explain what momentum, the per-coordinate scaling and the schedule each fix.
- Mention one thing that can go wrong.

:::feynman{id=f1 prompt="Explain why modern training uses Adam with warmup and a decaying learning rate instead of plain SGD, using the picture of a long narrow valley." key_points="The largest curvature limits the stable step size, so plain gradient descent crawls along flat directions|Momentum averages gradients so oscillations cancel and consistent directions accumulate speed|Adam divides each coordinate by a running root mean square of its gradients, making steps independent of gradient scale|Warmup avoids unstable large steps early, and decay shrinks the noise around the minimum later|A concrete failure such as too high a learning rate, missing bias correction or L2 instead of decoupled weight decay"}
:::
