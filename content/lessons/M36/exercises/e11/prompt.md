# REINFORCE in a gridworld

Train a tabular softmax policy on e07's $4 \times 4$ gridworld (provided) with episodes, returns-to-go and a learned baseline (Section 6). For each episode, walk backwards computing $G_t = r_t + \gamma G_{t+1}$; at each step update the state's baseline $V(s_t) \leftarrow V(s_t) + 0.1(G_t - V(s_t))$ and the logits $\theta_{s_t} \leftarrow \theta_{s_t} + \eta\,(G_t - V(s_t))(e_{a_t} - \pi(\cdot \mid s_t))$.

- `run_episode(P, pi, rng, max_steps=50)`: a list of `(s, a, r)` from the start state until the goal or `max_steps`.
- `train(P, gamma=0.95, episodes=600, lr=0.1, use_baseline=True, seed=0)`: return the logits.
- `policy(theta)`: the row-wise softmax.

The tests evaluate the learned policy exactly and find it within 0.5 of the optimal value from value iteration, about $-5.7$ from the start; the same training without the baseline ends far worse.

## Hints

1. Sample the next state with `rng.choice(S, p=P[a, s])`.
2. Sampling an action requires the probabilities of the current logits; compute the policy once per episode.
3. Returns-to-go use only rewards after the action: earlier rewards cannot be affected by it, so leaving them out only removes noise.
