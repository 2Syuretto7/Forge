# Find the unit error

A colleague estimated the GPU-hours of the training run from the Scale movement and reported 12,000 GPU-hours. The starter contains their code, `colleague_gpu_hours`, marked as provided. Do not change it.

- `gpu_hours(n_params, n_tokens, flops_per_s)` computes the correct GPU-hours at full utilization: $6ND$ over the rate, in hours.
- `error_factor(n_params, n_tokens, flops_per_s)` returns the colleague's answer divided by the correct one.
- `diagnose(ratio)` names the unit slip that explains a ratio between a wrong and a right answer. The starter's table `SLIPS` maps names to factors (seconds versus hours is 3,600, GB versus GiB is $2^{30}/10^9$, bits versus bytes is 8, and so on). Return the name whose factor is closest to `ratio` on a log scale, or `None` if even the closest is more than 2 percent away. A ratio below 1 is the same slip in the other direction: compare `max(ratio, 1/ratio)`.

## Hints

1. On a log scale, "closest" means the smallest `abs(math.log(ratio / factor))`.
2. Two percent away means `max(r / f, f / r) > 1.02`.
3. Run the colleague's function on the numbers in the tests to see their mistake.
