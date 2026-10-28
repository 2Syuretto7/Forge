# Puzzle: what should the model be rewarded for?

You have a model that answers questions, and a reward model trained on people's preferences between pairs of answers. You let a reinforcement-learning algorithm push the model toward answers the reward model scores highly.

::::predict{id=p1 kind=choice answer=c}
You optimize hard, with no constraint on how far the model may move. What usually happens to the true quality of its answers, as judged by people?

- It keeps rising with the reward model's score.
- It stays where it was: reward models are unbiased.
- It rises at first, then falls, while the reward model's score keeps rising.
- It falls immediately.

:::reveal
A reward model is a proxy, accurate on answers like those it was trained on and wrong on unusual ones. A strong optimizer finds the unusual answers it overrates: flattery, length, confident nonsense. Gao et al. (2023) measured exactly this rise-then-fall. RLHF therefore maximizes the reward **minus** a penalty on the KL divergence from the starting model, which keeps the policy where the reward model can be trusted. Move the penalty in the widget.
:::
::::

:::widget{name=RewardKLTradeoff}
:::

::::predict{id=p2 kind=choice answer=a}
In the widget, switch to optimizing the true reward. As the KL weight falls, true quality:

- Keeps rising, toward the best response's value.
- Rises, then falls.
- Falls.
- Stays constant.

:::reveal
With the true reward there is nothing to exploit: the optimum concentrates on the best response, and quality rises monotonically as the policy is allowed to move. The penalty matters most when the reward is imperfect, which in practice it always is, unless it can be checked exactly, as with math answers or unit tests (section 8).
:::
::::
