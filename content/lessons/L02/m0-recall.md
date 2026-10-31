# Recall bridge: estimators, held-out loss and ridge

This lesson stands on three earlier ones. From M25: estimators have bias and variance, and mean squared error is their sum. From M27: cross-entropy on held-out data measures a probabilistic model. From L01: least squares, ridge regression and standardization with training statistics only. Reviews due from those lessons appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
An estimator has bias $0.3$ and variance $0.16$. Its mean squared error is $0.3^2 + 0.16 =$ [[0.25]].
:::
:::step
Ridge regression in one dimension gives $\hat w = \sum x_i y_i / (\sum x_i^2 + \lambda)$. With $\sum x_i^2 = 10$ and $\lambda = 10$, the estimate is shrunk to a fraction [[0.5]] of the least-squares value.
:::
:::step
A model reaches a training loss of $0.9$ nats and a held-out loss of $1.4$ nats. The generalization gap is [[0.5]] nats.
:::
::::
