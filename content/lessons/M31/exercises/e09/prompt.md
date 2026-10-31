# Measuring a generalization gap

Train logistic regression with a small ridge penalty on $n$ examples in $d$ dimensions from the starter's `make_task(n, d, seed)`, and measure the **generalization gap**: test loss minus training loss (Section 2, and L02).

- `loss(w, X, y)` and `grad(w, X, y)`: the average logistic loss and its gradient (labels 0 and 1).
- `fit(X, y, lam=1e-3, steps=300)`: gradient descent on loss plus $\frac\lambda2\lVert w\rVert^2$ with step $4n/\lambda_{\max}(X^\top X)$ (the inverse of a smoothness bound, M28).
- `gap(n, d, seed=0)`: fit on `make_task(n, d, seed)` and return test loss on `make_task(5000, d, seed + 1000)` minus training loss.

The tests run a **gradient check** of `grad`, then show the gap shrinking as $n$ grows and growing with $d$, roughly like $d/n$.

## Hints

1. Stable softplus and sigmoid from M26.
2. The training loss is measured on the same data the model was fitted to; it is optimistic.
3. Average a few seeds when comparing gaps, since each is noisy.
