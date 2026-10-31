# A reward model from preferences

People compare two responses more reliably than they score one. The Bradley-Terry model turns comparisons into a reward: $P(a \succ b) = \sigma(r_a - r_b)$. With a linear reward $r = F w$ on response features:

1. `bt_loss(w, F_win, F_lose)`: the mean $-\log \sigma(r_\text{win} - r_\text{lose})$ over pairs, and its gradient.
2. `fit_bt(F_win, F_lose, steps=2000, lr=1.0)`: gradient descent from zero.

## Hints

1. $-\log \sigma(d) = \log(1 + e^{-d})$: `np.logaddexp(0, -d)`.
2. The gradient is $-\sum (F_\text{win} - F_\text{lose})^\top \sigma(-d)/n$.
3. Only differences of rewards are identified: adding a constant to every reward changes nothing.
