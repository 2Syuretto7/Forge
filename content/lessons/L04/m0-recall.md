# Recall bridge: likelihoods and softmax

This lesson stands on two earlier ones. From L02 it takes the likelihood and maximum likelihood; from M19 the softmax and its Jacobian. Due reviews from those lessons appear above. Then work through the short refresher below.

## From L02: the average log-likelihood

For data $x_1, \dots, x_n$ and a model $q$, the MLE maximizes $\frac{1}{n}\sum_i \log q(x_i)$. For categorical data with counts $c_j$ the maximizer is $q_j = c_j/n$.

## From M19: softmax and its Jacobian

$p = \operatorname{softmax}(z)$ with $p_i = e^{z_i}/\sum_k e^{z_k}$, Jacobian $\operatorname{diag}(p) - pp^\top$, and shift invariance $\operatorname{softmax}(z + c) = \operatorname{softmax}(z)$.

::::derivation{id=d0 title="Warm-up"}
:::step
A model assigns probability $0.25$ to the outcome that happened. Its negative log-likelihood for that outcome, in nats, is $-\ln 0.25 = \ln 4 \approx$ [[1.386]].
:::
:::step
The same quantity in bits is $\log_2 4 =$ [[2]].
:::
:::step
To convert nats to bits, divide by $\ln 2$. So $1$ nat is about [[1.4427]] bits.
:::
:::step
With logits $z = (2, 0)$, the softmax probability of the first class is $e^2/(e^2 + 1) \approx$ [[0.8808]].
:::
::::
