# Checking the GPU notebooks on a real T4

CI executes every notebook on a CPU in `SMALL=1` mode (Triton kernels in the interpreter), which
proves the code runs end to end but cannot run the tests that need a GPU: the speedups in L07, L08 and
L13, peak memory in L13, and the full-size training targets in L09 and L10. This check runs a solved
notebook on Colab's free T4 and compares its completion code with the code that every test passing
produces.

## Steps

1. Open one of the links below. Until a `main` branch exists, use the working branch name
   `ccr-4523d778-nctfqo` in place of `main`.
2. In Colab: **Runtime, Change runtime type, T4 GPU, Save**. (L04, L14, L17 and L19 also run on the CPU runtime.)
3. **Runtime, Run all**, and wait for the last cell.
4. The last cell prints one `PASS` line per test and then `Completion code: ...`. It should match the
   table. Any `FAIL` or `SKIP` line changes the code and names the test to look at.

| Notebook | Solved version | Expected code | Time on a T4 |
| --- | --- | --- | --- |
| L04 autograd vs PyTorch | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L04.ipynb` | `FORGE-L04-30720042` | under a minute |
| L07 roofline and profiling | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L07.ipynb` | `FORGE-L07-1dfab4d4` | a few minutes |
| L08 Triton and FlashAttention | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L08.ipynb` | `FORGE-L08-c7bb9175` | a few minutes (kernel compilation) |
| L09 transformer on Shakespeare | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L09.ipynb` | `FORGE-L09-9d81fa67` | about a minute |
| L10 GPT with BPE | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L10.ipynb` | `FORGE-L10-90d8f4e9` | a few minutes |
| L11 scaling laws | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L11.ipynb` | `FORGE-L11-674145ff` | about 10 minutes |
| L12 data pipeline | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L12.ipynb` | `FORGE-L12-ee0fc570` | a few minutes |
| L13 mixed precision | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L13.ipynb` | `FORGE-L13-1655992f` | a few minutes |
| L14 distributed training | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L14.ipynb` | `FORGE-L14-7160c856` | under a minute (CPU runtime is enough) |
| L15 pretraining run | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L15.ipynb` | `FORGE-L15-a8e54189` | 15 to 25 minutes |
| L16 fine-tuning with LoRA | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L16.ipynb` | `FORGE-L16-3acf8813` | about 5 minutes |
| L17 RL with a verifier | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L17.ipynb` | `FORGE-L17-07f097b7` | a few minutes |
| L18 inference server | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L18.ipynb` | `FORGE-L18-d67c421a` | about 5 minutes |
| L19 induction circuit | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L19.ipynb` | `FORGE-L19-cd1e77b9` | a few minutes |
| L20 the whole pipeline | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L20.ipynb` | `FORGE-L20-3cda1479` | 10 to 20 minutes |

If only one is checked, check **L08**: its Triton kernels are compiled for the GPU only there, while the
other notebooks use standard PyTorch operations whose CPU and GPU paths are the same code. If a second is
checked, check **L15**: its full run is the only one that could not be executed end to end on a CPU here.

## What has been verified without a GPU

- Every notebook runs to its autograder cell in CI (`npm run notebooks`), on PyTorch 2.8 CPU and
  Triton 3.4.
- The L09 and L10 notebooks were run at full size on a CPU: L09 reached a validation loss of 1.59
  nats per character (target 1.70) and L10 2.19 bits per character (target 2.3), with all tests
  passing. The L04 notebook was run at full size on a CPU, with its loss curve matching PyTorch to
  2e-16.
- The L08 kernels pass their tests in the Triton interpreter under Triton 3.4 and 3.8.
- The L11 and L12 notebooks were run at full size on a CPU with all tests passing (see the numbers in the
  lessons). The L14 notebook has no GPU part and passes in full under papermill. The L15 full run (5,000
  steps of a 10.7-million-parameter model) was not run end to end without a GPU. Its code was checked in the
  small configuration and in a medium one on a CPU (4 layers, width 128, 1,500 steps, corruption injected at
  position 900): the spike was flagged at position 900, the run rolled back to the checkpoint at step 750 and
  skipped to position 921, and the final validation loss (1.886) improved on the pre-spike value (2.108),
  with every test passing except the full-size loss target, which does not apply to that configuration.
- The L16, L17 and L19 notebooks were run at full size on a CPU with all tests passing. L16's LoRA model reached
  0.89 and 0.90 accuracy on the two tasks with 0.022 nats of forgetting; L17's weak-penalty policy raised sampled
  accuracy by 0.35 with a KL of 0.45 against 0.21 and 0.15 for the strong penalty; L19 found one previous-token
  head and four induction heads whose ablation sends the loss back to chance.
- The L18 notebook was run on a CPU with the full-size model (trained for only 20 steps, which does not change
  the serving measurements) and passed all tests: a 4.8x speedup at saturation, 20 ms 95th-percentile inter-token
  latency and 204 ms to first token, every served output matching recomputation. Int8 quality was checked
  separately on a trained model: validation loss changed by 0.0001 and 95% of greedy tokens were unchanged.
- The L20 notebook was run on a CPU in a medium configuration (4 layers, width 192, 2,000 pretraining steps) and
  passed all tests: validation loss 1.57, 97% greedy accuracy on capitals after fine-tuning, an RL gain in sampled
  reversal accuracy of 0.11 [0.08, 0.13], and serving that matched recomputation. Its full configuration (the
  10.8-million-parameter model for 3,000 steps) needs the T4.

The learner versions (`notebooks/<ID>.ipynb`, opened by the lesson's Colab button) have the solution
regions replaced by `NotImplementedError` and stop at the first one, as intended.
