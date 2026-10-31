# DPO

The KL-regularized objective $\max_\pi \mathbb{E}[r] - \beta\,\mathrm{KL}(\pi \,\|\, \pi_\text{ref})$ has the solution $\pi^* \propto \pi_\text{ref}\, e^{r/\beta}$, so $r = \beta \log(\pi^*/\pi_\text{ref}) + \text{const}$. Substituting into the Bradley-Terry likelihood gives DPO: fit the policy directly to preferences, with no reward model and no sampling.

1. `dpo_loss(lw, ll, lw_ref, ll_ref, beta)`: the mean of $-\log \sigma\bigl(\beta[(l_w - l_w^\text{ref}) - (l_l - l_l^\text{ref})]\bigr)$ and its gradients with respect to $l_w$ and $l_l$.
2. `tabular_dpo(ref, prefs, beta, steps=3000, lr=0.5)`: a policy $\operatorname{softmax}(\theta)$ over $K$ responses, starting at $\theta = \log \pi_\text{ref}$, trained on preference counts `(winner, loser, count)` by gradient descent through the log-softmax.

The tests generate preferences from a Bradley-Terry reward and check that DPO lands exactly on $\pi_\text{ref} e^{r/\beta}/Z$.

## Hints

1. With $s = \sigma(-z)$: $\partial/\partial l_w = -\beta s/n$ and $\partial/\partial l_l = +\beta s/n$.
2. Through the log-softmax, a gradient $g$ with respect to $\log \pi$ becomes $g - \pi \sum g$ with respect to $\theta$.
3. Weight each pair by its count divided by the total count.
