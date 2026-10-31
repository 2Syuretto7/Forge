# Break it: overflowing losses and the two KLs

## The textbook formula overflows

$\operatorname{softmax}(z)_i = e^{z_i}/\sum_k e^{z_k}$ is correct mathematics and broken arithmetic. In float64, $e^{710}$ overflows to infinity; in float32 the limit is $e^{89}$, and anything below about $e^{-104}$ underflows to zero. Logits of a few hundred are routine in an untrained or unstable network, and probabilities of $10^{-50}$ are routine for the wrong classes of a confident one.

::::predict{id=p5 kind=choice answer=c}
In float32, what does the naive computation $\log(\operatorname{softmax}(z)_1)$ return for $z = (0, -120)$?

- About $-120$, which is correct.
- About $-89$, clamped at the smallest float.
- $-\infty$, because the probability underflows to zero.
- `nan`, because of $\infty/\infty$.

:::reveal
$e^{-120} \approx 7.7 \times 10^{-53}$ is smaller than the smallest positive float32 (about $1.4 \times 10^{-45}$, a subnormal), so the probability is exactly zero and its log is $-\infty$. The stable form $z_1 - \operatorname{LSE}(z)$ never forms the probability and returns $-120$.
:::
::::

:::exercise{ref=e11}
:::

## Mass-covering and mode-seeking

Fit one Gaussian to a target with two peaks. The forward KL $\mathrm{KL}(p\|q)$ pays heavily wherever $p$ has mass and $q$ does not, so $q$ stretches to cover both peaks and puts its own peak in the empty valley between them. The reverse KL $\mathrm{KL}(q\|p)$ pays wherever $q$ has mass and $p$ does not, so $q$ retreats into one peak and ignores the other.

::::predict{id=p6 kind=sketch answer="0.36,0.63,0.89,1,0.89,0.63,0.36" xlabel="x from -3 to 3" ylabel="fitted density (scaled)"}
The target has peaks at $x = -2$ and $x = 2$. Sketch the Gaussian obtained by minimizing the **forward** KL, at $x = -3, -2, \dots, 3$, scaled so its maximum is 1.

:::reveal
Moment matching gives mean 0 and standard deviation $\sqrt{4 + 0.36} \approx 2.09$: a single broad bump centered in the valley at $x = 0$, where the target itself has almost no mass. Scaled values at $x = -3, \dots, 3$ are about $0.36, 0.63, 0.89, 1, 0.89, 0.63, 0.36$. That is the price of covering both modes with one Gaussian. The reverse-KL fit would instead be a narrow bump on one of the peaks.
:::
::::

:::exercise{ref=e10}
:::

## A zero in the wrong place

:::exercise{ref=e15}
:::

## Why this matters later

Maximum likelihood training minimizes the forward KL from data to model, so models trained this way are mass-covering: they put some probability on everything the data contains, which is why samples from them can be diverse and occasionally strange. RLHF in L21 adds a reverse KL from the policy to a reference model, which keeps the policy inside the region the reference finds plausible.

:::edge{to=L21 text="The KL penalty in RLHF is a reverse KL to the reference model."}
:::
