# Puzzle: how much momentum?

A ball rolling down a long valley picks up speed along the floor, which helps, and overshoots across the walls, which hurts. Momentum gives gradient descent the same behaviour: each step adds a fraction $\beta$ of the previous step.

::::predict{id=p1 kind=numeric answer=0.67 tol=0.04}
On a quadratic whose curvatures range from 1 to 100, what momentum $\beta$ makes the heavy-ball method converge fastest?

:::reveal
About $0.67$: $\beta^\star = \left(\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}\right)^2 = (9/11)^2$. Less momentum leaves the floor direction slow; more makes the steep directions oscillate. At the optimum every curvature contracts at the same rate, $\sqrt{\beta^\star} = 9/11$ per step.
:::
::::

::::predict{id=p2 kind=choice answer=b}
Gradient descent with its best step needs about 690 steps to reduce the error a millionfold at $\kappa = 100$. About how many does heavy ball with its best constants need?

- About 690: momentum changes the path, not the speed.
- About 70.
- About 7.
- About 350.

:::reveal
About 70: the rate improves from $\frac{\kappa - 1}{\kappa + 1}$ to $\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}$, so the step count scales with $\sqrt\kappa$ instead of $\kappa$. At $\kappa = 10^4$ that is the difference between 69,000 steps and 700.
:::
::::

Gradient descent, heavy ball and Nesterov, each with its best constants, on the same quadratic. Raise the condition number and watch the gap open; then take over the momentum and push it past the optimum.

:::widget{name=ConvergenceRates logkappa=2 iters=300}
:::

## Questions to carry into the derivation

1. What can be proved about gradient descent beyond quadratics?
2. Why is the optimal momentum the value it is, and why does it give $\sqrt\kappa$?
3. What happens when the gradient is only a noisy estimate?
4. Why does Adam correct its moving averages, and what goes wrong without it?
