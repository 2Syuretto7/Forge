# Adam, break it: an online problem Adam gets wrong

Adam's denominator forgets large gradients quickly. Reddi, Kale and Kumar built a problem where that is fatal (Section 5): on $x \in [-1, 1]$ the losses are $f_t(x) = Cx$ when $t \bmod 3 = 1$ and $-x$ otherwise, with $C = 3$. The average loss $\frac{C - 2}3x$ is minimized at $x = -1$, but with $\beta_1 = 0$ and $\beta_2 = 1/(1 + C^2)$, Adam drifts to $x = +1$: the rare large gradient is divided by a large $\sqrt v$, the frequent small ones by a small one. **AMSGrad** divides by the running maximum of $v$ instead and converges correctly.

- `online_grad(t, C=3.0)`.
- `run(amsgrad, steps=30000, C=3.0)`: projected Adam (or AMSGrad) with $\beta_1 = 0$, $\beta_2 = 1/(1 + C^2)$ and learning rate $0.5/\sqrt t$, from $x = 0$, clipping to $[-1, 1]$ after each step; return the final $x$.
- `average_loss_slope(C=3.0)`: $(C - 2)/3$.

The tests find Adam at $+1$, the worst point, and AMSGrad within 0.01 of $-1$.

## Hints

1. With $\beta_1 = 0$, $m_t = g_t$; only $v$ carries memory.
2. Keep $\hat v_t = \max(\hat v_{t-1}, v_t)$ for AMSGrad.
3. In practice $\beta_2 = 0.999$ makes such failures rare, but the example shows that Adam's convergence proof needed an assumption that can fail.
