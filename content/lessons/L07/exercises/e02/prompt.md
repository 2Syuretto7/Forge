# The roofline as code

1. `ridge(peak, bw)`: the intensity where the two roofs meet.
2. `roofline_time(flops, nbytes, peak, bw)`: the lower bound $\max(F/P, B/\text{BW})$ on a kernel's runtime.
3. `bound(flops, nbytes, peak, bw)`: `"memory"` if the kernel's intensity is below the ridge point, else `"compute"`.
4. `efficiency(flops, nbytes, measured_seconds, peak, bw)`: the roofline bound divided by a measured time, the fraction of the achievable speed a kernel reached.

`T4` holds the datasheet numbers.

## Hints

1. Every function is one line.
2. A kernel exactly at the ridge point is limited by both roofs equally; call it compute-bound.
3. An efficiency above 1 means a measurement or a count is wrong.
