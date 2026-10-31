# Puzzle: a narrow valley

Gradient descent zig-zags across a long, narrow valley: the steep walls force a small step, and along the gentle floor that small step makes slow progress.

::::predict{id=p1 kind=choice answer=c}
The valley becomes 10 times narrower: its level sets keep their length along the floor but become 10 times thinner across it. How does the number of gradient descent steps to reach a given accuracy change, with the best fixed step each time?

- It stays the same.
- About 3 times more.
- About 100 times more.
- About 10 times more.

:::reveal
About 100 times more. The width of a level set across the valley is proportional to $1/\sqrt{\text{curvature}}$, so 10 times thinner means 100 times the curvature across, and the condition number $\kappa = L/\mu$ grows a hundredfold. The step must stay below $2/L$, while progress along the floor is proportional to $\eta\mu$, so the number of steps grows in proportion to $\kappa$.
:::
::::

::::predict{id=p2 kind=numeric answer=690 tol=40}
On a quadratic with condition number 100, gradient descent with the best fixed step shrinks the error by a factor $\frac{\kappa - 1}{\kappa + 1} = \frac{99}{101}$ per step. About how many steps does it take to shrink it by a factor of a million?

:::reveal
About 690: $\ln(10^6)/\ln(101/99) \approx 13.8/0.020$. Each step removes only 2 percent of the error, and a factor of a million needs $13.8$ e-foldings at $0.02$ each. Momentum (M29) brings this down to about 70.
:::
::::

Watch the zig-zag. The valley here has condition number 10 and the step is just below $1/L$; raise the condition number and see how much longer the path along the floor becomes.

:::widget{name=LossLandscape surface=quadratic kappa=10 loglr=-1.05 beta=0.9}
:::

## Questions to carry into the derivation

1. Which functions have no bad local minima, and how can you tell?
2. What does the Hessian say about how fast gradient descent converges?
3. Why is the condition number the eigenvalue ratio of the Hessian, and why does iteration count grow with it?
4. How do you minimize under an equality constraint?
