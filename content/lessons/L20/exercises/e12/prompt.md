# Break it: the server sees different tokens

The model was trained on raw bytes. The serving front end tidies whitespace before encoding: it collapses runs of spaces and tabs and strips the ends. Nothing crashes, but the model now sees inputs unlike anything it trained on (verse indented with spaces, prompts ending in a newline). Both encoders are provided.

Implement `skew_report(samples)`: the fraction of samples whose encodings differ, and for the first such sample, its index and the first position where the token ids differ.

## Hints

1. Compare the two lists of ids; if one is a prefix of the other, the first difference is at the shorter length.
2. Train/serve skew is found by running the training encoder and the serving path on the same inputs and comparing, before launch.
3. The fix is one encoder, shared by training and serving, versioned with the model.
