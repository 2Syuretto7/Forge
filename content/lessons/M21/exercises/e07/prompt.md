# Monty Hall, simulated and solved

A prize is behind one of three doors. You pick door 0. The host, who knows where the prize is, opens another door with no prize (choosing at random when he can), and offers a switch.

- `simulate(n, switch, seed=0)`: the fraction of `n` games won, always switching or never.
- `bayes_switch_win()`: the exact probability of winning by switching, from Bayes' rule: hypotheses "prize behind door $k$", evidence "the host opens door 2".

Switching wins with probability $2/3$. The evidence is not "door 2 is empty" but "the host chose to open door 2", and its likelihood differs between hypotheses.

## Hints

1. Draw the prize door and, when there is a choice, the host's door with `rng.integers`.
2. Likelihoods of "host opens door 2": $\frac12$ if the prize is behind 0, $1$ if behind 1, $0$ if behind 2.
3. The switch goes to door 1.
