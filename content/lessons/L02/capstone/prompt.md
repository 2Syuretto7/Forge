# Capstone: double descent, reproduced and explained

`make_problem(seed)` in the starter builds the widget's setup: inputs in $\mathbb{R}^{200}$ with variances $\lambda_j = j^{-1.5}$, a target $y = \beta^\top x + \text{noise}$ with unit signal variance, $n = 20$ training points, and a $80 \times 200$ matrix `W` of random feature directions. The model with $p$ features uses $\phi(x) = W_{1:p}\,x$.

Implement:

1. `fit(Phi, y, lam)`: ridge with penalty `lam` in the scaled form of L01's `ridge` (minimize $\|\Phi w - y\|^2 + \lambda\|w\|^2$); use the minimum-norm interpolant when `lam == 0` and $p > n$, and least squares when `lam == 0` and $p \le n$.
2. `excess_risk(w, W_p, beta, lam_x)`: $(\beta - W_p^\top w)^\top \Sigma (\beta - W_p^\top w)$ with $\Sigma = \operatorname{diag}(\lambda_x)$.
3. `curve(ps, lam, seeds, noise)`: the average excess risk over the given seeds for each `p`, plus the average smallest singular value of the $n \times p$ feature matrix.
4. `peak(ps, risks)`: the `p` with the largest risk.
5. `REPORT`: at least 100 words explaining where the peak is, why (use your singular values), what happens with ridge, and why the right side can beat the left.

The tests check the curve against a reference implementation at several `p`, the peak location, the second descent, and that ridge removes the peak.
