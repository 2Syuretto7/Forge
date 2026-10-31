# Adam at scale: a badly scaled problem

On a quadratic whose curvatures span four orders of magnitude, gradient descent's learning rate is limited by the stiffest direction and crawls along the flattest; Adam's per-coordinate scaling moves all coordinates at a similar speed (Section 4). Count the steps each needs to bring every coordinate below $10^{-3}$.

- `steps_to_tol(run, tol=1e-3, max_steps=50000)`: the first step at which every coordinate's absolute value is below `tol`, given a function `run(steps)` returning a trajectory; `None` if never.
- `compare(scales, x0)`: a dict with the steps of gradient descent at its largest stable learning rate times 0.9, $1.8/\max s$, and of Adam with learning rate $0.01$ followed by a decay of 0.999 per step, using e12's runners (rewrite them here with the decay).

The tests use 50 coordinates with curvatures from $10^{-2}$ to $10^2$ and find Adam more than five times faster: gradient descent needs tens of thousands of steps, Adam a few hundred.

## Hints

1. A step decay $\eta_t = 0.01\cdot0.999^t$ lets Adam settle instead of oscillating at the scale of its step.
2. Gradient descent's slowest coordinate shrinks by $1 - \eta s_{\min}$ per step: with $\eta s_{\max} = 1.8$, that is $1 - 1.8\times10^{-4}$.
3. On a diagonal problem Adam's preconditioning is exact; on a rotated one it helps less, which is one reason second-order and whitening optimizers exist.
