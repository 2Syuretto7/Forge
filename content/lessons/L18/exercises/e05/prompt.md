# Continuous batching

Requests arrive over time and want different numbers of tokens. `requests` is a list of `(arrival_step, output_tokens)` sorted by arrival; the server decodes one token per running request per step.

1. `static_batching(requests, batch_size)`: when the server is free, take up to `batch_size` requests that have arrived (waiting for the first if none has) and run the batch until its longest request finishes. Return every request's finish step.
2. `continuous_batching(requests, batch_size)`: at every step, fill free slots with requests that have arrived, then every running request produces one token, and finished requests leave at once.

## Hints

1. In static batching a short request waits for the longest one in its batch, and new arrivals wait for the whole batch.
2. Keep the waiting queue in arrival order.
3. Continuous (iteration-level) batching, introduced by Orca (2022), is what every modern serving engine does.
