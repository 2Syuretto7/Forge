import { describe, expect, it } from 'vitest';
import { ARCHS, decodeStepSeconds, kvBytes, kvBytesPerToken, maxBatch } from '../../src/widgets/KVCacheMeter';
import { RESPONSES, expect as expectation, implicitReward, kl, optimalPolicy } from '../../src/widgets/RewardKLTradeoff';
import { evaluateSae, featureDirections, sampleActivations, trainSae } from '../../src/widgets/FeatureDictionary';

describe('KVCacheMeter', () => {
  it('bytes per token of published architectures', () => {
    expect(kvBytesPerToken(ARCHS.llama7, 2)).toBe(524288); // 0.5 MiB per token
    expect(kvBytesPerToken(ARCHS.mistral7, 2)).toBe(131072); // GQA: a quarter of that
    expect(kvBytesPerToken(ARCHS.llama70, 2)).toBe(327680);
    expect(kvBytes(ARCHS.llama7, 2, 8, 4096)).toBe(8 * 4096 * 524288);
  });

  it('capacity and decode time', () => {
    const cap = 80 * 2 ** 30;
    const b = maxBatch(ARCHS.llama7, 2, 2, 4096, cap);
    expect(ARCHS.llama7.params * 2 + kvBytes(ARCHS.llama7, 2, b, 4096)).toBeLessThanOrEqual(cap);
    expect(ARCHS.llama7.params * 2 + kvBytes(ARCHS.llama7, 2, b + 1, 4096)).toBeGreaterThan(cap);
    expect(maxBatch(ARCHS.llama70, 2, 2, 4096, cap)).toBe(0);
    expect(decodeStepSeconds(ARCHS.llama7, 2, 0, 2e12)).toBeCloseTo((6.74e9 * 2) / 2e12, 12);
  });
});

describe('RewardKLTradeoff', () => {
  const ref = RESPONSES.map((r) => r.ref);
  const proxy = RESPONSES.map((r) => r.proxy);
  const truth = RESPONSES.map((r) => r.truth);

  it('the optimum is a distribution that tends to the reference as beta grows', () => {
    expect(ref.reduce((a, b) => a + b, 0)).toBeCloseTo(1, 12);
    const pi = optimalPolicy(ref, proxy, 0.3);
    expect(pi.reduce((a, b) => a + b, 0)).toBeCloseTo(1, 12);
    const far = optimalPolicy(ref, proxy, 1e6);
    far.forEach((p, i) => expect(p).toBeCloseTo(ref[i], 5));
  });

  it('lower beta buys reward with KL', () => {
    const betas = [3, 1, 0.3, 0.1, 0.03];
    const pis = betas.map((b) => optimalPolicy(ref, proxy, b));
    for (let i = 1; i < pis.length; i++) {
      expect(kl(pis[i], ref)).toBeGreaterThan(kl(pis[i - 1], ref));
      expect(expectation(pis[i], proxy)).toBeGreaterThan(expectation(pis[i - 1], proxy));
    }
  });

  it('the implicit reward of DPO equals the reward up to a constant', () => {
    const pi = optimalPolicy(ref, proxy, 0.5);
    const imp = implicitReward(pi, ref, 0.5);
    const shift = imp[0] - proxy[0];
    imp.forEach((v, i) => expect(v - proxy[i]).toBeCloseTo(shift, 10));
  });

  it('optimizing the proxy too hard lowers true quality', () => {
    const moderate = optimalPolicy(ref, proxy, 1);
    const hard = optimalPolicy(ref, proxy, 0.02);
    expect(expectation(hard, proxy)).toBeGreaterThan(expectation(moderate, proxy));
    expect(expectation(hard, truth)).toBeLessThan(expectation(moderate, truth));
    expect(expectation(optimalPolicy(ref, truth, 0.02), truth)).toBeGreaterThan(0.9);
  });
});

describe('FeatureDictionary', () => {
  it('toy activations are sparse sums of feature directions', () => {
    const dirs = featureDirections(4);
    expect(dirs[1][0]).toBeCloseTo(0, 12);
    expect(dirs[1][1]).toBeCloseTo(1, 12);
    const data = sampleActivations(4, 0.1, 400, 3);
    const zeros = data.filter(([x, y]) => x === 0 && y === 0).length;
    expect(zeros / 400).toBeGreaterThan(0.5);
  });

  it('a sparse autoencoder recovers features that outnumber the dimensions', () => {
    for (const seed of [1, 2, 3]) {
      const d = sampleActivations(4, 0.15, 600, 10 + seed);
      const ev4 = evaluateSae(trainSae(d, 8, 10 ** -1.5, 1500, seed), d, 4);
      expect(ev4.recovered.every((c) => c > 0.95)).toBe(true);
    }
    const data = sampleActivations(4, 0.15, 600, 11);
    const sae = trainSae(data, 8, 10 ** -1.5, 1500, 5);
    const ev = evaluateSae(sae, data, 4);
    expect(ev.mse).toBeLessThan(0.02);
    sae.Wd.forEach(([a, b]) => expect(Math.hypot(a, b)).toBeCloseTo(1, 9));
  });
});
