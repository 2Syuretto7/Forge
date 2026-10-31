# Capstone: RL with a verifiable reward, and what the KL penalty buys

Open the Colab notebook with a **T4 GPU** runtime (a CPU runtime also finishes in a few minutes) and work through it:

1. Run the supervised fine-tuning on demonstrations with 30% slips, and compare its greedy and sampled accuracy on held-out sums.
2. Write `reward`, the exact-match reward on the text before the first newline.
3. Write `group_advantages`, each reward normalized within its group of samples for the same question.
4. Write `rl_loss`, the masked policy-gradient loss plus the KL penalty $\beta(e^u - 1 - u)$ with $u = \log\pi_\text{ref} - \log\pi$.
5. Train with penalties 0.01 and 1.0 and compare both with the supervised model, item by item, in sampled and greedy accuracy and in KL.
6. Write a report of at least 80 words: the supervised accuracies, each policy's gain with its interval and its KL, the tradeoff, and when a strong penalty is the right choice.

The autograder checks the reward, advantages and loss on small cases; that the weak penalty raises held-out sampled accuracy with a paired interval whose lower end exceeds **0.1**; that the strong penalty ends closer to the supervised model in KL and at least 0.05 less accurate when sampling; and the report.
