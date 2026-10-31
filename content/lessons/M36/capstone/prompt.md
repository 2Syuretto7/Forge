# Capstone: a policy-gradient agent with a measured baseline

The starter provides `make_world()`, the $5 \times 5$ gridworld of e07 with slip probability 0.1 and discount `GAMMA = 0.95`, together with `policy(theta)` and `run_episode(P, pi, rng)`.

1. `train(episodes=800, lr=0.1, seed=0)`: REINFORCE with returns-to-go and a learned baseline (e11); return `(theta, V)`, the logits and the learned state values.
2. `episode_gradient(theta, traj, V=None)`: as in e12, with `GAMMA`.
3. `gradient_variance(theta, V, n=400, seed=1)`: sample `n` episodes under `policy(theta)` and return a dict with the total variances `"without"` and `"with"` (using the learned `V`) and their ratio `"factor"`.
4. `optimal_value()`: $V^*$ at the start state, by value iteration (e07).
5. `REPORT`: at least 120 words. Report the learned policy's value against the optimum, the variance reduction factor and what it means for the number of episodes needed, and explain why subtracting a baseline that depends only on the state cannot bias the gradient.

The tests evaluate your policy exactly and require its value within 0.5 of the optimum, a variance reduction factor above 3, and estimates whose means agree.
