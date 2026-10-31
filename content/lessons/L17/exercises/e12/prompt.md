# Break it: no KL penalty

Implement `train_with_kl(means, beta, steps=2000, lr=0.5)`: exact policy-gradient ascent (no sampling) on $\mathbb{E}[r] - \beta\,\mathrm{KL}(\pi \,\|\, \pi_\text{ref})$ for a bandit, from the uniform reference. `entropy` is provided.

Without the penalty the policy collapses onto one action: its entropy goes to zero and it no longer produces anything else, which in a language model means one way of answering everything, and no exploration left for later training.

## Hints

1. Write the objective's gradient as $\pi \odot (f - \pi^\top f)$ with $f = r - \beta \log(\pi/\pi_\text{ref})$.
2. With $\beta > 0$ the iteration converges to $\pi_\text{ref} e^{r/\beta}/Z$.
3. Compare the entropies of the two runs.
