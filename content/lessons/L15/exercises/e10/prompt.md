# Watching update sizes

The ratio of an update's size to the parameter's size, $\|\Delta W\|/\|W\|$, says how far one step moves each layer. Around $10^{-3}$ is typical for Adam; much larger means the layer is moving too fast to be stable, much smaller that it has stopped learning.

1. `update_ratios(params, updates)`: a dictionary from each name to the ratio of Frobenius norms.
2. `flag_layers(ratios, low=1e-5, high=1e-2)`: the sorted names outside $[\text{low}, \text{high}]$.

## Hints

1. `np.linalg.norm` of a matrix is the Frobenius norm by default.
2. Compute the update as the parameter after the step minus before, so it includes weight decay and clipping.
3. Logging these per layer costs almost nothing and often points at the layer where a spike starts.
