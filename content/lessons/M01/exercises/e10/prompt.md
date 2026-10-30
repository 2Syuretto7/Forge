# GPU-hours for a pretraining run

Turn the training-cost rule into a planner.

- `tokens_for(n_params, tokens_per_param=20)` returns the number of training tokens for a model trained at a fixed number of tokens per parameter (20 is a common compute-efficient choice; L15 derives why).
- `gpu_hours(n_params, n_tokens, flops_per_s, utilization=0.4)` returns $6ND$ divided by the sustained rate `flops_per_s * utilization`, converted from seconds to hours.
- `wall_clock_days(n_gpu_hours, n_gpus)` returns the days the run takes on `n_gpus` GPUs working in parallel.
- `run_cost(n_gpu_hours, price_per_hour)` returns the cost in dollars.

Real runs never reach a GPU's peak: memory traffic, communication and data loading leave a typical utilization of 30 to 50 percent, so the default is 0.4.

## Hints

1. Seconds are FLOPs divided by FLOP/s; hours are seconds divided by 3,600.
2. Wall-clock time is total GPU-hours divided by the number of GPUs, then by 24.
3. Keep units in your variable names (`seconds`, `hours`) so a mistake shows.
