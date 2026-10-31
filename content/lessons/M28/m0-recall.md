# Recall bridge: from Hessians to the shape of a problem

M18 built the gradient and the Hessian, and M13 read a symmetric matrix through its eigenvalues. Put together, they describe the shape of a loss near any point: a bowl, a saddle, or a long narrow valley. This lesson asks which shapes are easy to optimize and how hard the hard ones are, and finds one property, convexity, and one number, the condition number, that answer both. Clear your due cards above first.

:::edge{from=M18 text="gradients and Hessians"}
:::

:::edge{from=M13 text="eigenvalues and positive definiteness"}
:::

## What carries over

The second-order Taylor expansion $f(x + h) \approx f(x) + \nabla f^\top h + \frac12 h^\top H h$ from M18; the spectral theorem and the test "positive definite means all eigenvalues positive" from M13; and from M16, gradient descent with step $\eta$ diverges once $\eta$ exceeds $2$ divided by the largest curvature.
