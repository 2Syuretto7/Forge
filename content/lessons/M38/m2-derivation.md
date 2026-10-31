# Derivation: three papers, from first principles

## 1. Reading a paper's mathematics

The method of this lesson, and of L20's paper audits, has four steps. **List the assumptions**, including the unstated ones: noise models, independence, ranks, step sizes. **Re-derive every equation** from the ones before it, writing next to each step the lesson it uses. **Reproduce the central claim** on a problem small enough that the right answer is known. **Break one assumption** on purpose and check that the claim fails in the way the derivation predicts. A derivation you can break where you expect is one you understand.

:::edge{to=L20 text="the paper audit method is applied to your capstone model."}
:::

## 2. DPO: preferences without a reward model

**Assumptions.** People's preferences follow the Bradley-Terry model, $P(y_w \succ y_l) = \sigma(r(y_w) - r(y_l))$ for some reward $r$; the goal is the KL-regularized objective of M36.

**Step 1 (M30).** The optimum of $\mathbb{E}_\pi[r] - \beta\,\mathrm{KL}(\pi\,\|\,\pi_{\text{ref}})$ is $\pi^*(y) = \pi_{\text{ref}}(y)e^{r(y)/\beta}/Z$.

**Step 2 (algebra).** Invert it: $r(y) = \beta\log\frac{\pi^*(y)}{\pi_{\text{ref}}(y)} + \beta\log Z$. The policy determines the reward up to a constant.

::::derivation{id=d1 title="An implied reward"}
:::step
If $\pi^*(y) = 0.5$, $\pi_{\text{ref}}(y) = 0.25$ and $\beta = 0.1$, the implied reward, up to the constant, is $0.1\ln 2 \approx$ [[0.0693|tol=0.0005]].
:::
::::

**Step 3 (M22, M27).** Fit Bradley-Terry by maximum likelihood: maximize $\sum\log\sigma(r_w - r_l)$, a cross-entropy over pairs. Only differences of rewards enter.

::::derivation{id=d2 title="A Bradley-Terry probability"}
:::step
A reward difference of 1 makes the preferred response win with probability $\sigma(1) \approx$ [[0.731|tol=0.001]].
:::
::::

**Step 4 (substitution).** Replace $r$ by the implied reward of the policy being trained. The constant $\beta\log Z$ cancels in the difference, and so does the reward model:

$$
\mathcal L_{\text{DPO}} = -\mathbb{E}\log\sigma\Big(\beta\log\frac{\pi(y_w)}{\pi_{\text{ref}}(y_w)} - \beta\log\frac{\pi(y_l)}{\pi_{\text{ref}}(y_l)}\Big) .
$$

**Step 5 (M36).** Its gradient is $\beta\,\sigma(-h)\,\nabla[\log\pi(y_w) - \log\pi(y_l)]$, with $h$ the margin inside: raise the winner, lower the loser, weighted by how wrong the policy currently is. It is REINFORCE-shaped, without sampling.

**What could break it.** If one response always wins, the maximum-likelihood margin is infinite: the loss has no minimum, and the KL regularization that motivated the method no longer acts.

## 3. LoRA: fine-tuning in a low-rank subspace

**Assumptions.** The weight update needed for fine-tuning, $\Delta W$, is close to low-rank; training the factors finds it.

**Step 1 (M14).** The best rank-$r$ approximation of $\Delta W$ is its truncated SVD, with error $(\sum_{j > r}\sigma_j^2)^{1/2}$. If the singular values fall fast, a small $r$ suffices.

**Step 2 (counting).** Writing $\Delta W = BA$ with $B \in \mathbb R^{k \times r}$, $A \in \mathbb R^{r \times d}$ costs $r(k + d)$ parameters instead of $kd$.

::::derivation{id=d3 title="Rank 8 on a 4096 by 4096 matrix"}
:::step
The trainable parameters number $8 \times (4096 + 4096) =$ [[65536]].
:::
::::

**Step 3 (M19).** Backpropagation through the product: with $G$ the gradient of the loss with respect to $W$, $\nabla_B = GA^\top$ and $\nabla_A = B^\top G$.

**Step 4 (initialization).** $B = 0$ and $A$ small and random make the model start exactly at $W_0$; the first steps move only $B$. After training, $W_0 + BA$ is merged into one matrix, at no inference cost.

**What could break it.** A full-rank update: then the loss at rank $r$ is bounded below by the discarded singular values, as Eckart-Young says.

## 4. Adam: moments, corrections and a counterexample

**Assumptions.** Gradients are noisy but their scale per coordinate changes slowly; exponential averages track the first and second moments.

**Step 1 (M22, M05).** $m_t = \beta_1m_{t-1} + (1 - \beta_1)g_t$ from $m_0 = 0$ gives $m_t = (1 - \beta_1)\sum_{s \le t}\beta_1^{t-s}g_s$. For a constant gradient the weights sum to $1 - \beta_1^t$, a geometric series, so $\hat m_t = m_t/(1 - \beta_1^t)$ is unbiased; likewise $\hat v_t$.

::::derivation{id=d4 title="Ten steps without correction"}
:::step
For a constant gradient 1 and $\beta_1 = 0.9$, the uncorrected average after 10 steps is $1 - 0.9^{10} \approx$ [[0.651|tol=0.001]].
:::
::::

**Step 2 (M29, M28).** The update $-\eta\,\hat m_t/(\sqrt{\hat v_t} + \varepsilon)$ divides each coordinate by an estimate of its gradient's size: a diagonal preconditioner, invariant to rescaling the loss, that equalizes the speeds of badly scaled coordinates.

::::predict{id=p3 kind=choice answer=b}
Adam's first step on a coordinate whose gradient is 250, with learning rate 0.01 and the bias corrections: how large is it?

- 2.5
- 0.01
- 0.0001
- It depends on $\beta_1$ and $\beta_2$.

:::reveal
$0.01$: at $t = 1$, $\hat m = g$ and $\hat v = g^2$, so the step is $\eta\,\mathrm{sign}(g)$, whatever the gradient's size. Without the corrections it would be $\eta(1 - \beta_1)/\sqrt{1 - \beta_2} \approx 3.16\eta$.
:::
::::

**Step 3 (convergence).** The paper's proof needed the effective step $\eta_t/\sqrt{\hat v_t}$ to be non-increasing. It need not be: Reddi, Kale and Kumar's online problem drives Adam to the worst point, and **AMSGrad**, which divides by the running maximum of $\hat v$, restores the guarantee.

::::derivation{id=d5 title="The first uncorrected step"}
:::step
With $\beta_1 = 0.9$ and $\beta_2 = 0.999$, the uncorrected first step is $(1 - 0.9)/\sqrt{1 - 0.999} \approx$ [[3.16|tol=0.01]] times the intended one.
:::
::::

:::edge{to=L20 text="audit a paper the same way: assumptions, derivation, reproduction, a deliberate break."}
:::

## Summary

| Paper | Central step | Lessons | Assumption to break |
| --- | --- | --- | --- |
| DPO | invert the Gibbs optimum; the reward cancels | M27, M30, M36 | preferences are noisy (Bradley-Terry) |
| LoRA | train $BA$ of rank $r$; Eckart-Young bounds the loss | M14, M19, M33 | the update is near low-rank |
| Adam | bias-corrected moments; per-coordinate scaling | M05, M16, M24, M29 | the effective step never grows |
