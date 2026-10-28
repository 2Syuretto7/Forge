# Host-to-device transfers

1. `transfer_time(nbytes, bw, latency_s=10e-6)`: a fixed latency plus bytes over bandwidth.
2. `effective_bandwidth(nbytes, bw, latency_s=10e-6)`: bytes divided by that time. Small copies never reach the link's bandwidth.
3. `input_pipeline_time(batch_bytes, compute_s, bw, overlap)`: the time per training step when each batch must be copied first; without overlap, copy then compute; with overlap (pinned memory and `non_blocking=True`, copying the next batch during this step), the larger of the two.

## Hints

1. PCIe 3.0 x16 peaks near 16 GB/s; about 12 GB/s is typical from pinned memory.
2. Half the link's bandwidth is reached when `nbytes / bw` equals the latency.
3. Overlap hides the copy completely only when it is shorter than the compute.
