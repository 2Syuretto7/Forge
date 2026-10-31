# Derivation: constrained optimization, duality and KKT

## 1. The Lagrangian

To minimize $f(x)$ subject to equality constraints $h_k(x) = 0$ and inequality constraints $g_j(x) \le 0$, form the **Lagrangian**

$$
\mathcal L(x, \lambda, \nu) = f(x) + \sum_j\lambda_j g_j(x) + \sum_k\nu_k h_k(x), \qquad \lambda_j \ge 0 .
$$

Each multiplier is a price charged for violating its constraint. For feasible $x$ and $\lambda \ge 0$, $\mathcal L \le f$, because every $\lambda_j g_j \le 0$ and every $h_k = 0$; maximizing over the multipliers recovers $f$ on feasible points and $+\infty$ elsewhere. So the constrained problem is $\min_x\max_{\lambda \ge 0, \nu}\mathcal L$.

::::derivation{id=d1 title="The closest point on a line"}
:::step
Minimize $x^2 + y^2$ subject to $x + 2y = 5$. Stationarity, $2x + \nu = 0$ and $2y + 2\nu = 0$, gives $y = 2x$, and the constraint then gives $x =$ [[1]].
:::
:::step
So $y =$ [[2]], and $\nu = -2$.
:::
::::

## 2. Inequality constraints and the KKT conditions

At a minimum of $f$ subject to $g(x) \le 0$, either the constraint is **inactive** ($g < 0$), and then the minimum is an ordinary unconstrained one with $\nabla f = 0$, or it is **active** ($g = 0$), and then $\nabla f$ must point into the feasible region's interior, opposite to $\nabla g$: $\nabla f = -\lambda\nabla g$ with $\lambda \ge 0$. Both cases are captured by the **Karush-Kuhn-Tucker conditions**:

1. stationarity: $\nabla f(x) + \sum_j\lambda_j\nabla g_j(x) + \sum_k\nu_k\nabla h_k(x) = 0$;
2. primal feasibility: $g_j(x) \le 0$, $h_k(x) = 0$;
3. dual feasibility: $\lambda_j \ge 0$;
4. complementary slackness: $\lambda_j g_j(x) = 0$ for every $j$.

For a convex problem (convex $f$ and $g_j$, affine $h_k$) with a strictly feasible point, they are necessary and sufficient for optimality. Complementary slackness says that a constraint costs nothing unless it binds.

::::derivation{id=d2 title="A bound that binds and one that does not"}
:::step
Minimize $(x - 3)^2$ subject to $x \le 1$. The minimum is $x = 1$, and stationarity $2(x - 3) + \lambda = 0$ gives $\lambda =$ [[4]].
:::
:::step
Subject to $x \le 5$ instead, the minimum $x = 3$ is interior and the multiplier is [[0]].
:::
::::

::::predict{id=p3 kind=choice answer=c}
At the optimum of a convex problem, a constraint has $g_j(x^\star) = -0.3$. What do you know about its multiplier?

- It is $0.3$.
- It is negative.
- It is exactly 0.
- It can be any nonnegative number.

:::reveal
Exactly 0, by complementary slackness: $\lambda_j g_j = 0$ with $g_j \ne 0$. The constraint has room to spare, so relaxing it changes nothing and its price is zero. A solver that reports a positive multiplier there has a bug, which the break movement asks you to find.
:::
::::

## 3. Duality

Minimizing the Lagrangian over $x$ for fixed multipliers gives the **dual function** $d(\lambda, \nu) = \min_x\mathcal L(x, \lambda, \nu)$, always concave, because it is a minimum of functions affine in the multipliers. Since $\mathcal L \le f$ on feasible points, every $d(\lambda, \nu)$ with $\lambda \ge 0$ is a lower bound on the optimal value: **weak duality**, $d^\star \le p^\star$. The **dual problem** maximizes that bound. For convex problems with a strictly feasible point (Slater's condition), **strong duality** holds: $d^\star = p^\star$, and the dual's maximizers are the KKT multipliers. The **duality gap** $f(x) - d(\lambda, \nu)$ of any feasible pair bounds how far $x$ is from optimal, which makes it the honest stopping rule for a solver.

Without convexity the gap can stay positive: a Boolean problem $\min x^\top Wx$ over $x \in \{-1, 1\}^n$ has a dual bound $n\lambda_{\min}(W)$ that is typically strictly below the true minimum.

::::derivation{id=d3 title="A dual by hand"}
:::step
Minimize $x^2$ subject to $1 - x \le 0$. The Lagrangian $x^2 + \lambda(1 - x)$ is minimized at $x = \lambda/2$, giving $d(\lambda) = \lambda - \lambda^2/4$, which is largest at $\lambda = 2$, where $d^\star =$ [[1]], equal to $p^\star = 1$.
:::
::::

## 4. Projected gradient descent

When the feasible set $C$ is simple, a box, a ball or the probability simplex, there is a cheaper route than multipliers: take a gradient step and project back, $x \leftarrow \Pi_C(x - \eta\nabla f(x))$, where $\Pi_C(y)$ is the closest point of $C$ to $y$. The projection is itself a tiny constrained problem whose KKT conditions have a closed form: clipping for a box, rescaling for a ball, and a single threshold $\theta$ with $\max(y - \theta, 0)$ for the simplex. Projected gradient descent keeps the convergence rates of M29 on convex problems.

## 5. The support vector machine and its dual

For labels $y_i = \pm1$, the **soft-margin SVM** finds $w$ minimizing $\frac12\lVert w\rVert^2 + C\sum_i\xi_i$ subject to $y_iw^\top x_i \ge 1 - \xi_i$ and $\xi_i \ge 0$: a wide margin $2/\lVert w\rVert$, with slack $\xi_i$ paid for points inside it. Its Lagrangian, minimized over $w$ and $\xi$, gives $w = \sum_i\alpha_iy_ix_i$ and the dual

$$
\max_{0 \le \alpha_i \le C}\ \sum_i\alpha_i - \frac12\Big\lVert\sum_i\alpha_iy_ix_i\Big\rVert^2 ,
$$

a quadratic over a box, which coordinate ascent solves one $\alpha_i$ at a time in closed form. Complementary slackness sorts the points: $\alpha_i = 0$ for points outside the margin, which do not affect $w$ at all; $0 < \alpha_i < C$ for points exactly on it; $\alpha_i = C$ for points inside it. The points with $\alpha_i > 0$ are the **support vectors**, usually a small fraction of the data.

::::derivation{id=d4 title="A margin"}
:::step
A separating $w$ with $\lVert w\rVert = 0.5$ has margin width $2/\lVert w\rVert =$ [[4]] between the lines $w^\top x = \pm1$.
:::
::::

:::edge{to=L01 text="ridge regression is a Lagrangian with a norm constraint."}
:::

## 6. Softmax from a constrained problem

Maximize $\sum_ip_ir_i + \tau H(p)$ over distributions $p$. With a multiplier $\nu$ for $\sum_ip_i = 1$ (the constraints $p_i \ge 0$ turn out inactive, because the entropy's slope is infinite at 0), stationarity reads $r_i - \tau(\log p_i + 1) - \nu = 0$, so

$$
p_i = \frac{e^{r_i/\tau}}{\sum_je^{r_j/\tau}} ,
$$

the **Gibbs distribution**: softmax at temperature $\tau$, the multiplier that prices certainty. As $\tau \to 0$ it concentrates on the best actions; as $\tau \to \infty$ it becomes uniform. The optimal value is $\tau\log\sum_je^{r_j/\tau}$, whose gradient is $p$ itself.

Replacing the entropy by a KL penalty toward a reference $\pi$, maximize $\sum_ip_ir_i - \beta\,\mathrm{KL}(p\,\|\,\pi)$. The same steps give

$$
p_i = \frac{\pi_ie^{r_i/\beta}}{\sum_j\pi_je^{r_j/\beta}} :
$$

the reference reweighted by exponentiated rewards. This is the optimum that RLHF aims at, and it can be inverted: $r_i = \beta\log(p_i/\pi_i) + \text{const}$, which is how DPO turns preferences between two answers into a loss on the policy alone.

::::derivation{id=d5 title="Two actions"}
:::step
Rewards 0 and 1 at temperature 1: the better action gets $e/(1 + e) \approx$ [[0.731|tol=0.001]].
:::
:::step
With a uniform reference and $\beta = 0.5$, the KL-regularized optimum gives it $e^2/(1 + e^2) \approx$ [[0.881|tol=0.001]].
:::
::::

:::edge{to=L17 text="the KL-regularized optimum returns as the basis of DPO."}
:::

:::edge{to=M38 text="reading objectives in research papers as constrained problems."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Lagrangian | $f + \sum\lambda_jg_j + \sum\nu_kh_k$, $\lambda \ge 0$ | prices for constraints |
| KKT | stationarity, feasibility, $\lambda \ge 0$, $\lambda_jg_j = 0$ | certify optimality |
| Weak duality | $d(\lambda, \nu) \le p^\star$ always | lower bounds, stopping rules |
| Strong duality | $d^\star = p^\star$ for convex problems with Slater | solve the easier problem |
| Projected gradient | step, then project onto $C$ | simple constraint sets |
| SVM dual | box-constrained QP; support vectors have $\alpha_i > 0$ | large-margin classifiers |
| Gibbs | $\max\ \mathbb{E}r + \tau H$ gives softmax at temperature $\tau$ | exploration, sampling |
| KL-regularized | $\max\ \mathbb{E}r - \beta\,\mathrm{KL}(p\|\pi)$ gives $\pi e^{r/\beta}/Z$ | RLHF, DPO |
