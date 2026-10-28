# Initialization from variance preservation

1. `xavier(n_in, n_out, rng)`: normal weights of shape `(n_in, n_out)` with variance $2/(n_{\text{in}} + n_{\text{out}})$.
2. `he(n_in, n_out, rng)`: variance $2/n_{\text{in}}$.
3. `depth_rms(init, act, depth=30, width=256, batch=128, seed=0)`: draw a batch of unit-normal inputs from `np.random.default_rng(seed)`, push it through `depth` layers $h \leftarrow \phi(hW)$ with fresh weights per layer from the same generator (`init` is `"xavier"`, `"he"` or `"unit"` for standard normal; `act` is `"relu"` or `"tanh"`), and return the root mean square of $h$ after each layer.

Then compare the six combinations. He with ReLU keeps the scale; Xavier with ReLU halves the second moment per layer; standard normal weights explode with ReLU and saturate tanh. Xavier with tanh shrinks slowly, about fivefold over 30 layers, because tanh is slightly contractive.

## Hints

1. `rng.normal(size=(n_in, n_out)) * np.sqrt(variance)`.
2. Use `np.tanh` or `np.maximum(z, 0)` for the activation.
3. RMS is `np.sqrt(np.mean(h * h))`.
