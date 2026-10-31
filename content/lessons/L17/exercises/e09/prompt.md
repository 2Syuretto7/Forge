# Verifiable rewards

For math and code the reward can be checked instead of learned: is the final answer right? DeepSeek-R1 and others trained reasoning with exactly such rewards, plus a format check, and normalized advantages within a group of samples for the same prompt (GRPO), with no value network.

1. `extract_answer(text)`: the last integer in the text (with an optional minus sign), or `None`.
2. `reward(text, answer, want_format=True)`: 1 for the right answer in the form `Answer: <n>` at the end; 0.5 for the right number without that format (when `want_format`); 0 otherwise.
3. `group_advantages(rewards, eps=1e-6)`: subtract the group's mean reward and divide by its standard deviation plus `eps`.

## Hints

1. `re.findall(r"-?\d+", text)` finds the integers.
2. A group where every sample got the same reward gives all-zero advantages: nothing to learn from that prompt.
3. Extraction rules are part of the reward: a lenient extractor rewards guessing, a strict one rewards formatting.
