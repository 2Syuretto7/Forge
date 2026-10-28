# Derivation: speed limits, momentum, adaptive steps, schedules and initialization

## 1. Gradient descent on a quadratic

Near a minimum $x^\star$, a smooth loss is approximately $f(x) = \tfrac12 (x - x^\star)^\top A (x - x^\star)$ with a symmetric positive definite Hessian $A$. The gradient is $A(x - x^\star)$, so the error $e_t = x_t - x^\star$ evolves as

$$
e_{t+1} = (I - \eta A)\, e_t.
$$

Write $A = Q \Lambda Q^\top$ (L01). In the eigenbasis the coordinates decouple: the component along eigenvector $q_i$ is multiplied by $1 - \eta \lambda_i$ at every step.

- The iteration converges if and only if $|1 - \eta\lambda_i| < 1$ for every $i$, that is $0 < \eta < 2/\lambda_{\max}$.
- The slowest component decides the rate $\rho(\eta) = \max_i |1 - \eta \lambda_i|$, which is smallest when the two extreme eigenvalues are balanced: $1 - \eta\mu = -(1 - \eta L)$, giving $\eta^\star = 2/(\mu + L)$ and

$$
\rho^\star = \frac{L - \mu}{L + \mu} = \frac{\kappa - 1}{\kappa + 1}, \qquad \kappa = L/\mu.
$$

::::derivation{id=d1 title="Rates on a valley with condition number 100"}
:::step
Take eigenvalues $\mu = 1$ and $L = 100$. With $\eta = 0.01$ the steep component is multiplied by $1 - 0.01 \cdot 100 =$ [[0]] per step and the flat component by [[0.99]].
:::
:::step
The best fixed rate is $\eta^\star = 2/101$, which gives contraction $\rho^\star = 99/101 \approx$ [[0.9802|tol=0.0005]] per step.
:::
:::step
To shrink the error by $10^{-6}$ you need $t$ with $(\rho^\star)^t = 10^{-6}$, about $\ln(10^6)/\ln(101/99) \approx$ [[691|tol=2]] steps. For large $\kappa$ this is about $\tfrac{\kappa}{2} \ln(1/\epsilon)$: the step count grows linearly with the condition number.
:::
::::

:::edge{from=L01 text="eigendecomposition of symmetric matrices and the condition number"}
:::

## 2. Momentum is a low-pass filter

Heavy-ball momentum keeps a velocity:

$$
v_{t+1} = \beta v_t + \nabla f(x_t), \qquad x_{t+1} = x_t - \eta v_{t+1}.
$$

Unrolled, $v_{t+1} = \sum_{k \ge 0} \beta^k \nabla f(x_{t-k})$: an exponentially weighted sum of past gradients. Feed it a signal $g_t = \cos(\omega t)$ and the steady-state output is a cosine of the same frequency with amplitude

$$
|H(\omega)| = \frac{1}{|1 - \beta e^{-i\omega}|}.
$$

At $\omega = 0$ (a gradient that keeps its sign) the gain is $1/(1 - \beta)$; at $\omega = \pi$ (a gradient that flips every step, the zig-zag across a valley) it is $1/(1 + \beta)$. Momentum amplifies the slow, consistent part of the gradient and suppresses the oscillating part.

::::derivation{id=d2 title="Gains and the optimal heavy ball"}
:::step
With $\beta = 0.9$, a constant gradient is amplified by [[10]] and an alternating one by $1/1.9 \approx$ [[0.526|tol=0.001]].
:::
:::step
On a quadratic, the best heavy-ball parameters are $\eta = 4/(\sqrt{L} + \sqrt{\mu})^2$ and $\beta = \left(\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}\right)^2$, and the error then shrinks by about $\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}$ per step. For $\kappa = 100$ that rate is $9/11 \approx$ [[0.8182|tol=0.0005]].
:::
:::step
Reducing the error by $10^{-6}$ then takes about $\ln(10^6)/\ln(11/9) \approx$ [[69|tol=1]] steps instead of 691: the step count grows like $\sqrt\kappa$ instead of $\kappa$.
:::
::::

The **exponential moving average** (EMA) $m_t = \beta m_{t-1} + (1 - \beta) g_t$ is the same filter scaled by $1 - \beta$, so its gain at frequency zero is exactly 1. Adam uses EMAs; heavy ball uses the unscaled sum. The two are equivalent up to a rescaling of $\eta$.

## 3. Adaptive steps: RMSProp and Adam

Momentum fixes the zig-zag but still uses one learning rate for every coordinate. **RMSProp** divides each coordinate's step by a running root mean square of its gradients, so steep coordinates take proportionally smaller steps. **Adam** combines this with momentum:

$$
m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t, \qquad v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2,
$$

$$
\hat m_t = \frac{m_t}{1 - \beta_1^t}, \qquad \hat v_t = \frac{v_t}{1 - \beta_2^t}, \qquad \theta_t = \theta_{t-1} - \eta \frac{\hat m_t}{\sqrt{\hat v_t} + \epsilon}.
$$

Typical values are $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$.

**Bias correction.** Both averages start at zero. If the gradients were constant, $g_t = g$, then $m_t = (1 - \beta_1^t) g$ exactly: the average is biased toward zero by the factor $1 - \beta_1^t$, which the division removes. The same holds for $v_t$ with $\beta_2$.

::::derivation{id=d3 title="The first Adam steps"}
:::step
With $\beta_1 = 0.9$, the first average is $m_1 = 0.1\, g_1$. After correction, $\hat m_1 =$ [[1]] times $g_1$.
:::
:::step
With correction, $\hat v_1 = g_1^2$, so the first step of each coordinate has magnitude $\eta |g_1| / |g_1| = \eta$, whatever the size of the gradient. Multiplying every gradient by $1000$ changes Adam's trajectory by a factor of [[1]] (ignoring $\epsilon$).
:::
:::step
Without correction, the first step is $\eta \cdot 0.1 g_1 / \sqrt{0.001 g_1^2}$, which is $0.1/\sqrt{0.001} \approx$ [[3.162|tol=0.002]] times too large.
:::
::::

Scale invariance is Adam's main appeal: one learning rate works across layers whose gradients differ by orders of magnitude. Its cost is memory, two extra numbers per parameter, which matters for large models.

## 4. Weight decay: L2 and decoupled

**L2 regularization** adds $\tfrac{\lambda}{2}\lVert\theta\rVert^2$ to the loss, so the gradient gains $\lambda\theta$. For plain SGD the update becomes $\theta \leftarrow (1 - \eta\lambda)\theta - \eta g$: the weights shrink by a constant factor per step. This is **weight decay**, and for SGD the two names describe the same thing.

For Adam they differ. Adding $\lambda\theta$ to the gradient sends it through the division by $\sqrt{\hat v}$, so a weight whose data gradient is large decays slowly and one whose gradient is tiny decays fast. **AdamW** (Loshchilov and Hutter) decouples the decay from the adaptive step:

$$
\theta_t = \theta_{t-1} - \eta \left( \frac{\hat m_t}{\sqrt{\hat v_t} + \epsilon} + \lambda \theta_{t-1} \right),
$$

with $\hat m, \hat v$ computed from the data gradient only. Every weight now shrinks by the factor $1 - \eta\lambda$ per step.

::::derivation{id=d4 title="Decay rates"}
:::step
SGD with $\eta = 0.1$ and L2 coefficient $\lambda = 0.01$ multiplies the weights by [[0.999]] per step before the gradient step.
:::
:::step
AdamW with $\eta = 0.01$ and $\lambda = 0.1$ over 1000 steps multiplies a weight with no consistent data gradient by about $0.999^{1000} \approx$ [[0.368|tol=0.002]].
:::
::::

## 5. Schedules

**Why decay.** With noisy gradients, SGD does not converge to the minimum but to a cloud around it. For $f(x) = \tfrac12 \lambda x^2$ with gradient noise of variance $\sigma^2$, the update $x \leftarrow (1 - \eta\lambda) x - \eta \xi$ has stationary variance

$$
\operatorname{Var}(x) = \frac{\eta^2\sigma^2}{1 - (1 - \eta\lambda)^2} = \frac{\eta \sigma^2}{\lambda(2 - \eta\lambda)},
$$

roughly proportional to $\eta$. A large rate makes fast progress but leaves a wide cloud; lowering it later shrinks the cloud.

**Why warm up.** At initialization the curvature can be much larger than later in training, and Adam's $\hat v$ rests on a handful of gradients. A linear ramp from zero to the peak rate over the first few hundred or thousand steps avoids early divergence.

**Warmup plus cosine.** With $W$ warmup steps, $T$ total steps, peak $\eta_{\max}$ and floor $\eta_{\min}$:

$$
\eta_t = \begin{cases} \eta_{\max}\, t/W & t < W, \\ \eta_{\min} + \tfrac12(\eta_{\max} - \eta_{\min})\left(1 + \cos\!\left(\pi \frac{t - W}{T - W}\right)\right) & W \le t \le T. \end{cases}
$$

::::derivation{id=d5 title="Noise floor and the cosine schedule"}
:::step
With $\lambda = 1$, $\sigma^2 = 1$ and $\eta = 0.1$, the stationary variance is $0.1/1.9 \approx$ [[0.0526|tol=0.0005]]. Halving $\eta$ to $0.05$ gives about [[0.0256|tol=0.0005]].
:::
:::step
With $\eta_{\max} = 0.003$, $\eta_{\min} = 0$, $W = 100$ and $T = 1100$, the rate at step 600, halfway through the decay, is [[0.0015]].
:::
::::

:::edge{to=L19 text="Warmup and the peak learning rate return when a large run spikes and has to be rewound."}
:::

:::edge{to=L15 text="Scaling laws assume a tuned rate and schedule per model size."}
:::

## 6. Initialization from variance preservation

L07 showed activations exploding or vanishing through depth. Make it exact. A layer computes $z_j = \sum_{i=1}^{n_{\text{in}}} W_{ij} x_i$ with independent zero-mean weights of variance $s^2$, independent of the inputs. Then

$$
\mathbb{E}[z_j^2] = n_{\text{in}}\, s^2\, \mathbb{E}[x_i^2].
$$

To keep the second moment constant through a linear layer, choose $s^2 = 1/n_{\text{in}}$. The same choice suits tanh, which is close to linear near zero; because tanh is slightly contractive, activations still shrink slowly with depth (exercise 7 measures about a factor of five over 30 layers). The backward pass multiplies gradients by $W^\top$, which asks for $s^2 = 1/n_{\text{out}}$; **Xavier (Glorot) initialization** compromises with $s^2 = 2/(n_{\text{in}} + n_{\text{out}})$.

ReLU zeroes the negative half of a symmetric input, so $\mathbb{E}[\operatorname{relu}(z)^2] = \tfrac12 \mathbb{E}[z^2]$. Keeping the second moment then needs $n_{\text{in}} s^2 \cdot \tfrac12 = 1$: **He initialization**, $s^2 = 2/n_{\text{in}}$.

::::derivation{id=d6 title="Initialization scales"}
:::step
For a ReLU layer with $n_{\text{in}} = 256$, He initialization uses standard deviation $\sqrt{2/256} =$ [[0.0884|tol=0.0002]].
:::
:::step
Using $s^2 = 1/n_{\text{in}}$ with ReLU instead multiplies the second moment by $\tfrac12$ per layer. After 40 layers it has shrunk by $2^{-40} \approx$ [[9.09e-13|tol=1e-14]].
:::
::::

:::widget{name=ActivationStats depth=30 init=xavier act=relu}
:::

In the widget, compare Xavier with He for ReLU and for tanh at depth 30; watch both the activations and the gradients.

:::edge{to=L10 text="Initialization sets the scale only at the start; normalization keeps it during training."}
:::

:::edge{from=L07 text="the MLP, its backward pass and the minibatch SGD loop"}
:::

:::edge{from=L08 text="parameters and gradients exposed by an autograd engine"}
:::

## Summary

| Method | Update | Fixes |
| --- | --- | --- |
| Gradient descent | $\theta \leftarrow \theta - \eta g$ | step limited by $2/L$; $\sim\kappa$ steps |
| Heavy ball | $v \leftarrow \beta v + g$, $\theta \leftarrow \theta - \eta v$ | zig-zag; $\sim\sqrt\kappa$ steps |
| Adam | $\theta \leftarrow \theta - \eta \hat m / (\sqrt{\hat v} + \epsilon)$ | per-coordinate scale |
| AdamW | adds $-\eta\lambda\theta$ outside the adaptive step | weight decay independent of gradient scale |
| Warmup and cosine | $\eta_t$ ramps up, then decays | early instability, late noise |
| Xavier, He | $s^2 = 2/(n_{\text{in}} + n_{\text{out}})$, $2/n_{\text{in}}$ | activation scale through depth |
