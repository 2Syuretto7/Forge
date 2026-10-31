# Capstone: FlashAttention in Triton

Open the Colab notebook with a **T4 GPU** runtime. After a worked vector-add kernel, write:

1. `softmax_kernel`: a fused row softmax (one program per row, computed in fp32).
2. `matmul_kernel`: a tiled matrix product with masked loads and stores and an fp32 accumulator.
3. `layernorm_kernel`: a fused layer norm forward pass.
4. `flash_kernel`: the forward pass of FlashAttention with the online softmax.

The autograder checks each kernel against PyTorch at sizes that are not multiples of the block sizes, checks your FlashAttention against unfused attention within $10^{-2}$ in fp16, and, on the GPU, that it is faster at sequence length 2048 with 16 heads of dimension 64.
