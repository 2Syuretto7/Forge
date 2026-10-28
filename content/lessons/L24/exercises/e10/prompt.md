# A pipeline you can audit

Six stages hand files to each other. When the final number looks wrong, you need to know exactly which data and configuration produced it. A **manifest** records, for each stage, a digest of what it read, of its configuration and of what it wrote. `digest` is provided.

1. `make_record(stage, input_digest, config, output)`.
2. `check_chain(records, first_input)`: the index of the first stage whose input is not the previous stage's output, or `None`.

## Hints

1. The first stage's input should be `first_input`, the digest of the raw data.
2. A broken link means a stage read a stale or different file: rerun from there.
3. Store the manifest with the final report and the model.
