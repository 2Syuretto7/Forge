# Puzzle: the faster you go, the slower you get

Take the narrow valley $f(x, y) = \tfrac12 (x^2 + 100 y^2)$ and run gradient descent from $(1, 1)$. A small learning rate crawls along $x$. You raise it, and progress along $x$ speeds up, until suddenly the iterates explode.

::::predict{id=p1 kind=numeric answer=0.02 tol=0.002}
What is the largest learning rate for which gradient descent on this valley does not diverge?

:::reveal
The gradient is $(x, 100 y)$, so one step multiplies $x$ by $1 - \eta$ and $y$ by $1 - 100\eta$. The $y$ coordinate stays bounded only if $|1 - 100\eta| < 1$, that is $\eta < 2/100 = 0.02$. The steep direction sets the speed limit, and at that limit the shallow direction shrinks by only 2 percent per step: more than 100 steps per factor of 10.
:::
::::

That is the whole problem of optimization in one picture: the step size must suit the steepest direction, so it is too small for the flattest one. A real network's loss has millions of directions whose curvatures span many orders of magnitude.

::::predict{id=p2 kind=choice answer=b}
Momentum adds a fraction $\beta$ of the previous step to each new step. What does it do in this valley?

- It multiplies every step by $1/(1 - \beta)$, which is the same as a larger learning rate.
- It cancels the back-and-forth steps across the narrow direction and accumulates speed along the long direction.
- Nothing useful: the zig-zag gets worse because old steps point the wrong way.
- It makes the iteration diverge for any learning rate.

:::reveal
Across the valley the gradient flips sign every step, so successive contributions cancel in the running sum; along the valley it keeps the same sign, so contributions add up to $1/(1 - \beta)$ times one step. Momentum is a low-pass filter on the gradient sequence, and the derivation makes this exact. A larger learning rate cannot do the same thing, because it amplifies both directions.
:::
::::

:::widget{name=LossLandscape surface=quadratic kappa=50 loglr=-1.8 beta=0.9}
:::

In the widget, raise the learning rate until plain SGD starts to zig-zag and then diverge, and compare the momentum and Adam trajectories at the same setting. Then switch to the Rosenbrock valley, whose curvature changes along the way.
