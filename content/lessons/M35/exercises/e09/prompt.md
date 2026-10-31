# The loss surface L(N, D)

The Chinchilla form models loss as a function of parameters $N$ and training tokens $D$ (Section 6, L11):

$$
L(N, D) = E + \frac A{N^\alpha} + \frac B{D^\beta} .
$$

Fitted directly, $A$ and $\alpha$ are nearly collinear, because $\ln N$ varies little relative to its size. Reparametrize around reference sizes $N_0 = 10^9$ and $D_0 = 10^{10}$: with $u = \ln(N/N_0)$ and $v = \ln(D/D_0)$, write $L = E + e^{a - \alpha u} + e^{b - \beta v}$ and fit $\theta = (E, a, \alpha, b, \beta)$.

- `surface(theta, N, D)` and `grad_surface(theta, N, D)`: the model and its Jacobian, one row per run and one column per parameter.
- `fit_surface(N, D, L, theta0, iters=200)`: Levenberg-Marquardt as in e05.
- `to_chinchilla(theta)`: `(E, A, alpha, B, beta)`, using $A = e^aN_0^\alpha$ and $B = e^bD_0^\beta$.

The tests run a **gradient check**, then fit 64 noisy runs on an $8 \times 8$ grid generated from the published Chinchilla fit ($E = 1.69$, $A = 406.4$, $\alpha = 0.34$, $B = 410.7$, $\beta = 0.28$) and recover both exponents within 0.03.

## Hints

1. $\partial L/\partial a = e^{a - \alpha u}$ and $\partial L/\partial\alpha = -u\,e^{a - \alpha u}$.
2. A start of $(2, -1, 0.3, -1, 0.3)$ works for these data.
3. Centering $u$ and $v$ near the data makes the columns of the Jacobian far less collinear: the same trick as centering a regressor.
