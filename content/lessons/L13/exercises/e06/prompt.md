# A dynamic loss scaler

Complete `DynamicLossScaler.update(found_inf)`, the rule PyTorch's `GradScaler` follows after each step:

- if the gradients contained an infinity or NaN, multiply the scale by `backoff`, reset the count of good steps, and return `False` (skip the update);
- otherwise count the good step, and when the count reaches `interval`, multiply the scale by `growth` and reset the count; return `True`.

## Hints

1. The skipped step does not count as good.
2. Growth happens on the step that completes the interval.
3. With the defaults, an overflow every few thousand steps keeps the scale near the largest safe value.
