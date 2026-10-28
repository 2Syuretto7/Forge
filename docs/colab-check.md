# Checking the GPU notebooks on a real T4

CI executes every notebook on a CPU in `SMALL=1` mode (Triton kernels in the interpreter), which
proves the code runs end to end but cannot run the tests that need a GPU: the speedups in L11, L12 and
L17, peak memory in L17, and the full-size training targets in L13 and L14. This check runs a solved
notebook on Colab's free T4 and compares its completion code with the code that every test passing
produces.

## Steps

1. Open one of the links below. Until a `main` branch exists, use the working branch name
   `ccr-4523d778-nctfqo` in place of `main`.
2. In Colab: **Runtime, Change runtime type, T4 GPU, Save**. (L08 also runs on the CPU runtime.)
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
| L17 mixed precision | `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/solved/L17.ipynb` | `FORGE-L17-834b5911` | a few minutes |

If only one is checked, check **L12**: its Triton kernels are compiled for the GPU only there, while the
other notebooks use standard PyTorch operations whose CPU and GPU paths are the same code.

## What has been verified without a GPU

- Every notebook runs to its autograder cell in CI (`npm run notebooks`), on PyTorch 2.8 CPU and
  Triton 3.4.
- The L13 and L14 notebooks were run at full size on a CPU: L13 reached a validation loss of 1.59
  nats per character (target 1.70) and L14 2.19 bits per character (target 2.3), with all tests
  passing. The L08 notebook was run at full size on a CPU, with its loss curve matching PyTorch to
  2e-16.
- The L12 kernels pass their tests in the Triton interpreter under Triton 3.4 and 3.8.

The learner versions (`notebooks/<ID>.ipynb`, opened by the lesson's Colab button) have the solution
regions replaced by `NotImplementedError` and stop at the first one, as intended.
