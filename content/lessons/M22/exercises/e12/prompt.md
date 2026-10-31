# Variance through fifty layers

Section 6 predicts that a linear layer with $n$ inputs and weights of variance $s^2/n$ multiplies the second moment of its inputs by $s^2$, and a ReLU after it halves it. Check the prediction through many layers.

- `layer_second_moments(depth, width, scale, activation="linear", batch=256, seed=0)`: start from a `(batch, width)` array of standard normal inputs, then `depth` times multiply by a fresh `(width, width)` weight matrix of standard normals times `scale / sqrt(width)`, applying `np.maximum(h, 0)` after each layer when `activation == "relu"`. Return the list of the mean squared activation after each layer. Draw everything from `np.random.default_rng(seed)`, inputs first.
- `preserving_scale(activation)`: the `scale` that keeps the second moment constant: 1 for linear layers and $\sqrt2$ for ReLU.
- `predicted_factor(scale, activation, depth)`: the predicted ratio of the last second moment to the input's, $(s^2)^L$, or $(s^2/2)^L$ with ReLU.

## Hints

1. The second moment of the standard normal inputs is 1, so the list itself shows the growth.
2. For ReLU, the first layer's input is a standard normal, not a ReLU output; the halving happens after every layer, the first included.
3. Twenty percent too large a scale multiplies the second moment by $1.44$ per layer: $1.44^{50} \approx 8 \times 10^7$.

At finite width each layer's factor fluctuates around its mean by a few percent, so after 50 layers the second moment can wander by a factor of several even at the right scale. The tests therefore measure the average factor per layer, the 50th root of the last second moment, and require it within 10 percent of the prediction.
