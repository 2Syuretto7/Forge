import { describe, expect, it } from 'vitest';
import { FORMATS, encode, epsilon, minNormal, minSubnormal, roundTo, type FormatId } from '../../src/widgets/FloatFormats';
import { HARDWARE, attainable, intensity, kernels, ridge } from '../../src/widgets/Roofline';
import { attention, makeQK, rowEntropyBits, softmaxRows } from '../../src/widgets/AttentionHeatmap';
import { SPACE, bpeEncode, bpeTrain, pretokenize } from '../../src/widgets/TokenizerStepper';

// Reference casts computed with PyTorch 2.14 (float64 -> dtype -> float64).
const XS = [
  0.1, 1 / 3, Math.PI, 1 + 2 ** -11, 1 + 3 * 2 ** -11, 1000, 65504, 65519, 65520, 70000, 1e-5, 1e-8, 3e-8, 3e38, 3.4e38, 460, 470, 500, 57344, 61000, 2 ** -9,
  1.5 * 2 ** -10, -2.7, 1e-40, 1e-45,
];
const INF = Infinity;
const TORCH: Record<FormatId, number[]> = {
  fp32: [
    0.10000000149011612, 0.3333333432674408, 3.1415927410125732, 1.00048828125, 1.00146484375, 1000, 65504, 65519, 65520, 70000, 9.999999747378752e-6, 9.99999993922529e-9,
    2.999999892949745e-8, 3.0000000054977558e38, 3.3999999521443642e38, 460, 470, 500, 57344, 61000, 0.001953125, 0.00146484375, -2.700000047683716, 9.99994610111476e-41,
    1.401298464324817e-45,
  ],
  bf16: [
    0.10009765625, 0.333984375, 3.140625, 1, 1, 1000, 65536, 65536, 65536, 70144, 1.0013580322265625e-5, 1.0011717677116394e-8, 3.003515303134918e-8, 3.00405527047391e38, INF,
    460, 470, 500, 57344, 60928, 0.001953125, 0.00146484375, -2.703125, 9.183549615799121e-41, 0,
  ],
  fp16: [
    0.0999755859375, 0.333251953125, 3.140625, 1, 1.001953125, 1000, 65504, 65504, INF, INF, 1.0013580322265625e-5, 0, 5.960464477539063e-8, INF, INF, 460, 470, 500, 57344,
    60992, 0.001953125, 0.00146484375, -2.69921875, 0, 0,
  ],
  e5m2: [
    0.09375, 0.3125, 3, 1, 1, 1024, INF, INF, INF, INF, 1.52587890625e-5, 0, 0, INF, INF, 448, 448, 512, 57344, 57344, 0.001953125, 0.00146484375, -2.5, 0, 0,
  ],
  e4m3: [
    0.1015625, 0.34375, 3.25, 1, 1, 448, 448, 448, 448, 448, 0, 0, 0, 448, 448, 448, 448, 448, 448, 448, 0.001953125, 0.001953125, -2.75, 0, 0,
  ],
};

describe('phase 3 widget numerics', () => {
  it('float rounding matches PyTorch casts for every format', () => {
    for (const id of Object.keys(FORMATS) as FormatId[]) {
      XS.forEach((x, i) => expect([id, x, roundTo(x, FORMATS[id])]).toEqual([id, x, TORCH[id][i]]));
    }
  });

  it('format constants are the standard ones', () => {
    expect(FORMATS.fp16.max).toBe(65504);
    expect(FORMATS.e5m2.max).toBe(57344);
    expect(FORMATS.e4m3.max).toBe(448);
    expect(FORMATS.bf16.max).toBeCloseTo(3.3895313892515355e38, -30);
    expect(minNormal(FORMATS.fp16)).toBe(2 ** -14);
    expect(minSubnormal(FORMATS.fp16)).toBe(2 ** -24);
    expect(epsilon(FORMATS.bf16)).toBe(2 ** -7);
    expect(minSubnormal(FORMATS.e4m3)).toBe(2 ** -9);
  });

  it('encodes bit fields', () => {
    expect(encode(1, FORMATS.fp16)).toEqual({ sign: 0, expField: 15, manField: 0, kind: 'normal' });
    expect(encode(-2.5, FORMATS.fp16)).toEqual({ sign: 1, expField: 16, manField: 256, kind: 'normal' });
    expect(encode(2 ** -24, FORMATS.fp16)).toEqual({ sign: 0, expField: 0, manField: 1, kind: 'subnormal' });
    expect(encode(1e6, FORMATS.fp16).kind).toBe('inf');
    expect(encode(448, FORMATS.e4m3)).toEqual({ sign: 0, expField: 15, manField: 6, kind: 'normal' });
  });

  it('roofline: attainable throughput and the ridge point', () => {
    const t4 = HARDWARE.t4;
    expect(ridge(t4.peak.fp16, t4.bw)).toBeCloseTo(203.125, 6);
    expect(attainable(t4.peak.fp16, t4.bw, 1)).toBe(320e9);
    expect(attainable(t4.peak.fp16, t4.bw, 1e4)).toBe(65e12);
    const ks = kernels(1024, 2);
    expect(intensity(ks[0])).toBeCloseTo(1 / 6, 12); // vector add in fp16
    expect(intensity(ks[ks.length - 1])).toBeCloseTo(2048 / 6, 9); // matmul: 2n^3 / (3 n^2 * 2 bytes)
  });

  it('attention: rows are distributions, the mask hides the future', () => {
    const { Q, K } = makeQK('random', 16, 1);
    const V = K.map((_, i) => [i, 2 * i]);
    const { weights, out } = attention(Q, K, V, { causal: true, scaled: true });
    weights.forEach((row, i) => {
      expect(row.reduce((a, b) => a + b, 0)).toBeCloseTo(1, 12);
      row.forEach((w, j) => (j > i ? expect(w).toBe(0) : expect(w).toBeGreaterThan(0)));
    });
    expect(weights[0][0]).toBe(1);
    expect(out[0]).toEqual([0, 0]);
    expect(softmaxRows([[0, Math.log(3)]], false)[0][1]).toBeCloseTo(0.75, 12);
  });

  it('attention: unscaled logits saturate as d grows, scaled ones do not', () => {
    const meanEntropy = (d: number, scaled: boolean) => {
      const { Q, K } = makeQK('random', d, 1);
      const w = attention(Q, K, K, { causal: false, scaled }).weights;
      return w.reduce((a, r) => a + rowEntropyBits(r), 0) / w.length;
    };
    expect(meanEntropy(256, false)).toBeLessThan(0.3);
    expect(meanEntropy(256, true)).toBeGreaterThan(1.5);
    expect(Math.abs(meanEntropy(256, true) - meanEntropy(16, true))).toBeLessThan(1);
  });

  it('attention: the previous-token head looks one step back', () => {
    const { Q, K } = makeQK('previous', 64, 6);
    const w = attention(Q, K, K, { causal: true, scaled: true }).weights;
    for (let i = 1; i < w.length; i++) expect(w[i].indexOf(Math.max(...w[i]))).toBe(i - 1);
  });

  it('BPE: merges the most frequent pair and replays merges on new text', () => {
    const { merges, steps } = bpeTrain('aaab aaab ab', 10);
    expect(merges[0].pair).toEqual(['a', 'a']);
    expect(steps[0].join('')).toBe(`aaab${SPACE}aaab${SPACE}ab`);
    for (const s of steps) expect(s.join('')).toBe(steps[0].join(''));
    expect(steps[steps.length - 1].length).toBeLessThan(steps[0].length);
    const enc = bpeEncode('aaab', merges.map((m) => m.pair));
    expect(enc.join('')).toBe('aaab');
    expect(enc.length).toBeLessThan(4);
  });

  it('BPE: word pre-tokenization keeps merges inside words', () => {
    expect(pretokenize('the cat  sat', true)).toEqual(['the', `${SPACE}cat`, `${SPACE}sat`]);
    const across = bpeTrain('ab ab ab ab', 10, false).merges.map((m) => m.pair.join(''));
    const within = bpeTrain('ab ab ab ab', 10, true).merges.map((m) => m.pair.join(''));
    expect(across.some((t) => t.includes(`b${SPACE}`))).toBe(true);
    expect(within.some((t) => t.includes(`b${SPACE}`))).toBe(false);
  });
});
