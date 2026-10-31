# Explain it plainly: why steps must shrink

Explain why noisy gradients force the step size down over time.

Guidelines:

- Write 150 to 400 words.
- Use a ball on a bowl that is kicked randomly at every step.
- Say what a constant step reaches, and what decides its size.
- Say what a good schedule must satisfy.

:::feynman{id=f1 prompt="Explain why noisy gradients force the step size down over time." key_points="A stochastic gradient is the true gradient plus noise, so each step moves toward the minimum and also kicks the iterate randomly|The pull toward the minimum is proportional to the step size, while the variance of the kick is proportional to the step size squared|With a constant step the two balance at a noise floor whose size is proportional to the step size times the gradient-noise variance, so the iterates never settle at the minimum|Shrinking the step lowers the floor, and steps whose sum is infinite but whose squares sum to a finite total, such as 1/k, drive the error to zero|Larger batches reduce the gradient variance and so lower the floor, but do not remove it"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove the descent lemma: if f is L-smooth, then f(x - grad f(x)/L) <= f(x) - |grad f(x)|^2 / (2L)." key_points="States the quadratic upper bound f(y) <= f(x) + grad f(x)^T (y - x) + (L/2)|y - x|^2, obtained from L-smoothness by integrating the gradient along the segment|Substitutes y = x - grad f(x)/L|Computes the linear term as -|grad f(x)|^2 / L|Computes the quadratic term as (L/2)|grad f(x)|^2 / L^2 = |grad f(x)|^2 / (2L)|Adds them to get the decrease of at least |grad f(x)|^2 / (2L)"}
:::
