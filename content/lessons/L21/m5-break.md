# Break it: hacking the reward, losing the leash

## A flawed reward

:::exercise{ref=e11}
:::

## No penalty

::::predict{id=p4 kind=choice answer=d}
You remove the KL penalty from an RL run with a reward that is correct but sparse. After many steps, the policy's entropy is:

- Unchanged.
- Higher, because the policy explores more.
- Exactly that of the reference.
- Near zero: it answers every prompt the same way, and has stopped exploring alternatives.

:::reveal
Policy gradients concentrate probability on whatever earned reward, and nothing pushes back. The policy collapses toward deterministic answers. This can look fine on the training reward, but diversity is gone, later training has nothing to explore, and on imperfect rewards the collapse is onto the exploit. Exercise 12 measures it.
:::
::::

:::exercise{ref=e12}
:::

## What to take away

- Use a baseline: group means or a value function cut the variance of policy gradients.
- Keep a KL penalty to the starting model, and watch KL alongside the reward.
- Check true quality on held-out evaluations; a rising reward is not enough.
- Prefer rewards you can verify; when you cannot, expect the policy to find the reward model's mistakes.
