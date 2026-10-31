# DPO, step 3: the loss

Substitute e01's implied reward into e02's likelihood. The constant $\beta\log Z$ cancels in the difference, and the reward model disappears (Section 2):

$$
\mathcal L_{\text{DPO}}(\pi) = -\sum_{(w, l)}\log\sigma\Big(\beta\Big[\log\frac{\pi(y_w)}{\pi_{\text{ref}}(y_w)} - \log\frac{\pi(y_l)}{\pi_{\text{ref}}(y_l)}\Big]\Big) .
$$

For a softmax policy with logits $z$ over $K$ responses, $\log\pi = z - \log\sum e^z$, and the normalizer cancels in the difference too, so the gradient in $z$ only involves the winner and the loser.

- `log_softmax(z)`.
- `dpo_loss(z, ref_logp, N, beta)`: the mean loss over all comparisons, from the count matrix $N$ of e02.
- `grad_dpo_loss(z, ref_logp, N, beta)`.

The tests run a **gradient check** of the loss in the logits.

## Hints

1. With $h_{ij} = \beta[(\log\pi_i - \log\pi_{\text{ref}, i}) - (\log\pi_j - \log\pi_{\text{ref}, j})]$, the loss is $\sum_{ij}N_{ij}\log(1 + e^{-h_{ij}})/\sum N$.
2. $\partial h_{ij}/\partial z = \beta(e_i - e_j)$: the softmax normalizer cancels.
3. Work with $K \times K$ arrays; no loop over comparisons is needed.
