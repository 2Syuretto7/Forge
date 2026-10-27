# Break it: precision, Hilbert matrices and squared condition numbers

You now know that $\kappa$ bounds error growth. This movement makes the bound bite: you will watch float32 return garbage, and you will watch the normal equations lose half of float64's digits on a problem that QR solves cleanly.

## Why precision and conditioning multiply

A solver that is **backward stable** (Gaussian elimination with pivoting, Householder QR) returns the exact answer to a nearby problem: the computed $\hat x$ solves $(A + \delta A)\hat x = b$ with $\|\delta A\| / \|A\|$ about $\varepsilon$. Combining that with Section 7 gives the rule of thumb

$$
\frac{\|\hat x - x\|}{\|x\|} \lesssim \kappa(A)\, \varepsilon .
$$

For the Hilbert matrix of size 6, $\kappa \approx 1.5 \times 10^7$. In float32, $\varepsilon \approx 6 \times 10^{-8}$, so the bound is about $0.9$. In float64, about $2 \times 10^{-9}$.

::::predict{id=p6 kind=choice answer=c}
You solve the least-squares problem for a $50 \times 6$ matrix with $\kappa(A) = 10^6$, once through the normal equations and once through QR, both in float64. Which outcome do you expect?

- Both have relative error near $10^{-16}$.
- Both have relative error near $10^{-10}$.
- QR near $10^{-10}$, normal equations near $10^{-4}$.
- The normal equations are more accurate because they solve a smaller square system.

:::reveal
QR works with $A$ itself, so its error tracks $\kappa(A)\varepsilon \approx 10^{-10}$. Forming $A^\top A$ squares the condition number to $10^{12}$, and $10^{12} \times 10^{-16} = 10^{-4}$. The normal equations throw away six digits before the solver even starts.
:::
::::

:::exercise{ref=e14}
:::

## What to take away

- Before trusting a solution, estimate $\kappa$. `np.linalg.cond` is cheap for small matrices.
- Never form $A^\top A$ when you can factor $A$. Library least-squares routines use QR or the SVD for this reason.
- Lower precision is not just "a bit less accurate": it caps which problems are solvable at all. L17 builds mixed-precision training on exactly this reasoning, keeping sensitive accumulations in higher precision.

:::aside[A detail about the float32 experiment]
Your solver performs every operation in float32, including the computation of $b = H\mathbf{1}$. So the problem you actually solve is already a rounded version of the intended one. That is realistic: data stored in float32 has already been rounded before any algorithm touches it.
:::
