# Running the film backwards

The forward process $dx = -x\,dt + \sqrt2\,dW$ has a time reversal, found by Anderson (Section 7): run from $t = T$ down to 0,

$$
dx = \big[-x - 2\nabla\log p_t(x)\big]\,dt + \sqrt2\,d\bar W ,
$$

where $dt$ is now negative. Started from samples of $p_T \approx N(0, 1)$, it ends with samples of the data. One Euler-Maruyama step from $t$ to $t - h$ is $x \leftarrow x + h\,(x + 2\nabla\log p_t(x)) + \sqrt{2h}\,z$.

- `time_grid(T, steps, tmin=1e-3)`: `steps + 1` times from $T$ down to `tmin`, geometrically spaced, so the steps are short where the score changes fast.
- `reverse_sample(score, n, T, steps, rng, tmin=1e-3)`: start from $N(0, 1)$ and apply the reverse steps; `score(x, t)` is vectorized over `x`.
- `w1(x, y)`: the one-dimensional Wasserstein distance between two equal-sized samples, the mean absolute difference of their sorted values.

The tests use the exact score of e05's noised mixture and find the generated samples within 0.06 of fresh data in $W_1$, where the starting noise is more than 0.8 away.

## Hints

1. `np.geomspace(T, tmin, steps + 1)`.
2. Use the current time $t_i$ for the score in the step from $t_i$ to $t_{i+1}$.
3. Near $t = 0$ the score of a narrow component is steep: geometric spacing puts many short steps there.
