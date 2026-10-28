# Checking the GPU notebooks on a real T4

CI executes every notebook on a CPU in `SMALL=1` mode (Triton kernels in the interpreter), which
proves the code runs end to end but cannot run the tests that need a GPU: the speedups in L11, L12 and
L17, peak memory in L17, and the full-size training targets in L13 and L14. This check runs a solved
notebook on Colab's free T4 and compares its completion code with the code that every test passing
produces.

## Steps

1. Open one of the links below. Until a `main` branch exists, use the working branch name
   `ccr-4523d778-nctfqo` in place of `main`.
2. In Colab: **Runtime, Change runtime type, T4 GPU, Save**. (L08, L18, L21 and L23 also run on the CPU runtime.)
3. **Runtime, Run all**, and wait for the last cell.
4. The last cell prints one `PASS` line per test and then `Completion code: ...`. It should match the
   table. Any `FAIL` or `SKIP` line changes the code and names the test to look at.

| Notebook | Solved version | Expected code | Time on a T4 |
| --- | --- | --- | --- |
| L08 autograd vs PyTorch | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L08.ipynb` | `FORGE-L08-a50eda67` | under a minute |
| L11 roofline and profiling | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L11.ipynb` | `FORGE-L11-241bf136` | a few minutes |
| L12 Triton and FlashAttention | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L12.ipynb` | `FORGE-L12-6d95f88b` | a few minutes (kernel compilation) |
| L13 transformer on Shakespeare | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L13.ipynb` | `FORGE-L13-b101ab3f` | about a minute |
| L14 GPT with BPE | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L14.ipynb` | `FORGE-L14-d11ba1e3` | a few minutes |
| L15 scaling laws | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L15.ipynb` | `FORGE-L15-6198b0a9` | about 10 minutes |
| L16 data pipeline | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L16.ipynb` | `FORGE-L16-eb661704` | a few minutes |
| L17 mixed precision | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L17.ipynb` | `FORGE-L17-834b5911` | a few minutes |
| L18 distributed training | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L18.ipynb` | `FORGE-L18-4b32bd11` | under a minute (CPU runtime is enough) |
| L19 pretraining run | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L19.ipynb` | `FORGE-L19-6ce319d2` | 15 to 25 minutes |
| L20 fine-tuning with LoRA | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L20.ipynb` | `FORGE-L20-4bd4514e` | about 5 minutes |
| L21 RL with a verifier | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L21.ipynb` | `FORGE-L21-9363f36f` | a few minutes |
| L22 inference server | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L22.ipynb` | `FORGE-L22-26986541` | about 5 minutes |
| L23 induction circuit | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L23.ipynb` | `FORGE-L23-2e7d993b` | a few minutes |
| L24 the whole pipeline | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L24.ipynb` | `FORGE-L24-bf03fbd2` | 10 to 20 minutes |

If only one is checked, check **L12**: its Triton kernels are compiled for the GPU only there, while the
other notebooks use standard PyTorch operations whose CPU and GPU paths are the same code. If a second is
checked, check **L19**: its full run is the only one that could not be executed end to end on a CPU here.

## What has been verified without a GPU

- Every notebook runs to its autograder cell in CI (`npm run notebooks`), on PyTorch 2.8 CPU and
  Triton 3.4.
- The L13 and L14 notebooks were run at full size on a CPU: L13 reached a validation loss of 1.59
  nats per character (target 1.70) and L14 2.19 bits per character (target 2.3), with all tests
  passing. The L08 notebook was run at full size on a CPU, with its loss curve matching PyTorch to
  2e-16.
- The L12 kernels pass their tests in the Triton interpreter under Triton 3.4 and 3.8.
- The L15 and L16 notebooks were run at full size on a CPU with all tests passing (see the numbers in the
  lessons). The L18 notebook has no GPU part and passes in full under papermill. The L19 full run (5,000
  steps of a 10.7-million-parameter model) was not run end to end without a GPU. Its code was checked in the
  small configuration and in a medium one on a CPU (4 layers, width 128, 1,500 steps, corruption injected at
  position 900): the spike was flagged at position 900, the run rolled back to the checkpoint at step 750 and
  skipped to position 921, and the final validation loss (1.886) improved on the pre-spike value (2.108),
  with every test passing except the full-size loss target, which does not apply to that configuration.
- The L20, L21 and L23 notebooks were run at full size on a CPU with all tests passing. L20's LoRA model reached
  0.89 and 0.90 accuracy on the two tasks with 0.022 nats of forgetting; L21's weak-penalty policy raised sampled
  accuracy by 0.35 with a KL of 0.45 against 0.21 and 0.15 for the strong penalty; L23 found one previous-token
  head and four induction heads whose ablation sends the loss back to chance.
- The L22 notebook was run on a CPU with the full-size model (trained for only 20 steps, which does not change
  the serving measurements) and passed all tests: a 4.8x speedup at saturation, 20 ms 95th-percentile inter-token
  latency and 204 ms to first token, every served output matching recomputation. Int8 quality was checked
  separately on a trained model: validation loss changed by 0.0001 and 95% of greedy tokens were unchanged.
- The L24 notebook was run on a CPU in a medium configuration (4 layers, width 192, 2,000 pretraining steps) and
  passed all tests: validation loss 1.57, 97% greedy accuracy on capitals after fine-tuning, an RL gain in sampled
  reversal accuracy of 0.11 [0.08, 0.13], and serving that matched recomputation. Its full configuration (the
  10.8-million-parameter model for 3,000 steps) needs the T4.

The learner versions (`notebooks/<ID>.ipynb`, opened by the lesson's Colab button) have the solution
regions replaced by `NotImplementedError` and stop at the first one, as intended.
