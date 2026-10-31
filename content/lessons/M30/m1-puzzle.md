# Puzzle: the most uncertain distribution with a given reward

Four actions pay rewards 1, 2, 3 and 4. You choose a distribution over them whose expected reward is 3, and among all such distributions you want the one with the highest entropy: the least committed choice that still earns 3 on average.

::::predict{id=p1 kind=choice answer=b}
What does that distribution look like?

- Uniform over the four actions.
- Probabilities growing exponentially with the reward: $p_i \propto e^{\beta r_i}$ for some $\beta > 0$.
- All mass on action 3.
- Probabilities growing linearly with the reward.

:::reveal
Exponential in the reward: Lagrange multipliers for the two constraints (probabilities sum to 1, expected reward 3) turn the stationarity condition into $\log p_i = \text{const} + \beta r_i$. That is softmax, with $1/\beta$ as its temperature; the uniform distribution has expected reward 2.5, too little.
:::
::::

::::predict{id=p2 kind=numeric answer=0.731 tol=0.01}
Two actions with rewards 0 and 1, at temperature 1: the Gibbs distribution $p_i \propto e^{r_i/\tau}$ gives the better action what probability?

:::reveal
$e/(1 + e) \approx 0.731$. At temperature $0.1$ it would be about $0.99995$; at temperature 10, about $0.525$. The temperature prices certainty: it is the multiplier on the entropy.
:::
::::

Move the free minimum of the quadratic around the constraint. While the free minimum is feasible the constraint is slack and its multiplier is 0; once it leaves, the constrained minimum sticks to the boundary, and the gradient of the objective is balanced by a positive multiple of the constraint's gradient.

:::widget{name=KKTGeometry constraint=halfplane cx=1.6 cy=1.2 level=1}
:::

## Questions to carry into the derivation

1. What replaces $\nabla f + \lambda\nabla g = 0$ when the constraint is an inequality?
2. What problem do the multipliers themselves solve, and when does it give the same answer?
3. Why are only a few training points needed to define a support vector machine?
4. Why does maximizing reward with an entropy or KL penalty produce exponentials?
