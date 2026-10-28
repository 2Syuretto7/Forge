# The RL stage: advantages and a penalized policy gradient

The RL stage samples several answers per prompt, scores them with an exact-match reward, and pushes up the better ones while a KL penalty keeps the policy near the fine-tuned reference (L21). `log_softmax` is provided.

1. `group_advantages(rewards)`: each reward normalized within its group.
2. `pg_loss(logits, actions, adv, ref_logits, beta)`: the loss $\operatorname{mean}\bigl(-A \log \pi(a) + \beta(e^u - 1 - u)\bigr)$ with $u = \log \pi_\text{ref}(a) - \log \pi(a)$, and its gradient with respect to the logits.

## Hints

1. A group whose answers all score the same gives zero advantages: there is nothing to learn from it.
2. $\partial \log \pi(a)/\partial z = \text{onehot}(a) - \pi$.
3. The penalty's derivative with respect to $\log \pi(a)$ is $1 - e^u$; it is zero where policy and reference agree.
