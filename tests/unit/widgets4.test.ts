import { describe, expect, it } from 'vitest';
import { CHINCHILLA, fitPower, fitPowerFloor, frontier, lossAt, optimal, predict, sampleRuns } from '../../src/widgets/ScalingFit';
import {
  MODELS,
  activationsPerLayer,
  bubbleFraction,
  dpTraffic,
  modelStates,
  paramCount,
  planMemory,
  tpTraffic,
  type Plan,
} from '../../src/widgets/ParallelismPlanner';
import { LOGS, detectSpikes, ema, rollbackPoint } from '../../src/widgets/LossSpikeExplorer';

describe('ScalingFit', () => {
  it('the closed-form allocation is the minimum over model sizes at fixed compute', () => {
    for (const C of [1e18, 1e21, 5.76e23]) {
      const opt = optimal(CHINCHILLA, C);
      expect(6 * opt.N * opt.D).toBeCloseTo(C, -Math.log10(C) + 9);
      let best = Infinity;
      let bestN = 0;
      for (let i = 0; i <= 20000; i++) {
        const N = 10 ** (5 + (9 * i) / 20000);
        const l = lossAt(CHINCHILLA, N, C / (6 * N));
        if (l < best) [best, bestN] = [l, N];
      }
      expect(opt.loss).toBeLessThanOrEqual(best + 1e-12);
      expect(Math.abs(opt.loss - best)).toBeLessThan(1e-6);
      expect(Math.abs(bestN / opt.N - 1)).toBeLessThan(0.002);
    }
  });

  it('the frontier is exactly E + K (C/6)^-gamma', () => {
    const f = frontier(CHINCHILLA);
    expect(f.gamma).toBeCloseTo((0.34 * 0.28) / 0.62, 12);
    for (const C of [1e17, 1e20, 1e25]) expect(f.E + f.K * (C / 6) ** -f.gamma).toBeCloseTo(optimal(CHINCHILLA, C).loss, 10);
  });

  it('fits recover the parameters of noiseless data', () => {
    const pure: [number, number][] = [1e18, 1e19, 1e20, 1e21].map((c) => [c, 30 * c ** -0.05]);
    const p = fitPower(pure);
    expect(p.k).toBeCloseTo(30, 8);
    expect(p.gamma).toBeCloseTo(0.05, 10);
    const runs = sampleRuns(CHINCHILLA, 18, 22, 8, 0);
    const f = fitPowerFloor(runs);
    const truth = frontier(CHINCHILLA);
    expect(Math.abs(f.E - truth.E)).toBeLessThan(2e-3);
    expect(Math.abs(f.gamma - truth.gamma)).toBeLessThan(2e-3);
  });

  it('a pure power law fitted on a narrow range extrapolates worse than one with a floor', () => {
    const runs = sampleRuns(CHINCHILLA, 18, 21, 8, 0);
    const target = 1e24;
    const truth = optimal(CHINCHILLA, target).loss;
    const errPure = Math.abs(predict(fitPower(runs), target) / truth - 1);
    const errFloor = Math.abs(predict(fitPowerFloor(runs), target) / truth - 1);
    expect(errPure).toBeGreaterThan(0.03);
    expect(errFloor).toBeLessThan(0.002);
    // The pure power law always predicts too low: it has no floor to slow down at.
    expect(predict(fitPower(runs), target)).toBeLessThan(truth);
  });
});

describe('ParallelismPlanner', () => {
  it('parameter counts of the presets', () => {
    expect(paramCount(MODELS.m124)).toBe(12 * 12 * 768 ** 2 + 50257 * 768);
    expect(paramCount(MODELS.m124) / 1e6).toBeCloseTo(123.5, 1);
    expect(paramCount(MODELS.b175) / 1e9).toBeCloseTo(174.56, 2);
  });

  it('ZeRO memory matches Figure 1 of Rajbhandari et al. (7.5B parameters, 64 GPUs)', () => {
    const total = (z: number) => Object.values(modelStates(7.5e9, z, 64)).reduce((a, b) => a + b, 0) / 1e9;
    expect(total(0)).toBeCloseTo(120, 6);
    expect(total(1)).toBeCloseTo(31.4, 1);
    expect(total(2)).toBeCloseTo(16.6, 1);
    expect(total(3)).toBeCloseTo(1.875, 6);
  });

  it('activation memory per layer', () => {
    expect(activationsPerLayer(2048, 1, 12288, 96, 1, false)).toBe(2048 * 12288 * (34 + 80));
    expect(activationsPerLayer(2048, 1, 12288, 96, 8, true)).toBe((2048 * 12288 * 34) / 8);
  });

  const base: Plan = { model: MODELS.b6_7, dp: 8, tp: 1, pp: 1, zero: 0, micro: 1, seq: 2048, accum: 8, checkpoint: false, flash: true };

  it('1F1B: the first stage stores as many layer activations as the unpipelined model', () => {
    const one = planMemory(base).activations;
    const four = planMemory({ ...base, pp: 4 }).activations;
    expect(four).toBeCloseTo(one, 6);
    expect(planMemory({ ...base, pp: 4 }).psi).toBeCloseTo(paramCount(MODELS.b6_7) / 4, 6);
  });

  it('checkpointing keeps only layer inputs plus one rebuilt layer', () => {
    const m = MODELS.b6_7;
    const ck = planMemory({ ...base, checkpoint: true }).activations;
    expect(ck).toBe(m.layers * 2 * 2048 * m.d + activationsPerLayer(2048, 1, m.d, m.heads, 1, true));
    expect(ck).toBeLessThan(planMemory(base).activations / 5);
  });

  it('bubble and traffic', () => {
    expect(bubbleFraction(1, 8)).toBe(0);
    expect(bubbleFraction(4, 8)).toBeCloseTo(3 / 11, 12);
    expect(dpTraffic(1e9, 0, 1)).toBe(0);
    expect(dpTraffic(1e9, 2, 8)).toBeCloseTo(3.5e9, 3);
    expect(dpTraffic(1e9, 3, 8)).toBeCloseTo(5.25e9, 3);
    expect(tpTraffic(base)).toBe(0);
    const tp = { ...base, tp: 2 };
    expect(tpTraffic(tp)).toBe(4 * 32 * 8 * 1 * 2 * 2048 * 4096);
  });
});

describe('LossSpikeExplorer', () => {
  it('flags a jump above the trailing mean plus k standard deviations', () => {
    const loss = Array.from({ length: 100 }, (_, i) => 2 + 0.01 * Math.sin(i));
    loss[60] = 2.5;
    expect(detectSpikes(loss, 20, 5)).toEqual([61]);
    expect(detectSpikes(loss, 20, 100)).toEqual([]);
    expect(detectSpikes(loss.slice(0, 20), 20, 5)).toEqual([]);
  });

  it('rolls back to a checkpoint saved before the update that preceded the flagged loss', () => {
    expect(rollbackPoint(700, 100)).toBe(600);
    expect(rollbackPoint(701, 100)).toBe(600);
    expect(rollbackPoint(702, 100)).toBe(700);
  });

  it('the logged runs share their history until the injected event', () => {
    const { healthy, bad_data, lr_bug } = LOGS.runs;
    for (const r of Object.values(LOGS.runs)) {
      expect(r.loss.length).toBe(1200);
      for (const key of ['loss', 'gradNorm', 'lr', 'maxLogit'] as const) expect(r[key].every(Number.isFinite)).toBe(true);
    }
    expect(bad_data.loss.slice(0, 699)).toEqual(healthy.loss.slice(0, 699));
    expect(lr_bug.loss.slice(0, 700)).toEqual(healthy.loss.slice(0, 700));
    expect(Math.abs(lr_bug.lr[699] / healthy.lr[699] / 20 - 1)).toBeLessThan(1e-3);
  });

  it('the detector finds the injected events and nothing in the healthy run', () => {
    const { healthy, bad_data, lr_bug } = LOGS.runs;
    expect(detectSpikes(healthy.loss, 50, 5)).toEqual([]);
    expect(detectSpikes(bad_data.loss, 50, 5)[0]).toBe(700);
    expect(detectSpikes(lr_bug.loss, 50, 5)[0]).toBe(701);
    // The learning-rate bug does lasting damage; the corrupted shard much less.
    const finalVal = (r: typeof healthy) => r.val[r.val.length - 1][1];
    expect(finalVal(lr_bug) - finalVal(healthy)).toBeGreaterThan(0.3);
    expect(finalVal(bad_data) - finalVal(healthy)).toBeLessThan(0.05);
  });

  it('QK-layernorm keeps attention logits small at a high learning rate', () => {
    const { high_lr, high_lr_qknorm } = LOGS.runs;
    expect(Math.max(...high_lr.maxLogit)).toBeGreaterThan(100);
    expect(Math.max(...high_lr_qknorm.maxLogit)).toBeLessThan(30);
    expect(high_lr_qknorm.val[high_lr_qknorm.val.length - 1][1]).toBeLessThan(high_lr.val[high_lr.val.length - 1][1]);
  });

  it('moving average', () => {
    expect(ema([1, 1, 1], 0.9)).toEqual([1, 1, 1]);
    expect(ema([0, 10], 0.9)[1]).toBeCloseTo(1, 12);
  });
});

describe('LshCurve', () => {
  it('candidate probabilities and thresholds', async () => {
    const { candidateProbability, lshThreshold, factorizations } = await import('../../src/widgets/LshCurve');
    expect(candidateProbability(0.8, 16, 8)).toBeCloseTo(1 - (1 - 0.8 ** 8) ** 16, 12);
    expect(candidateProbability(0.8, 16, 8)).toBeCloseTo(0.947, 3);
    expect(candidateProbability(0.5, 16, 8)).toBeCloseTo(0.0607, 4);
    expect(lshThreshold(16, 8)).toBeCloseTo(Math.SQRT1_2, 12);
    expect(factorizations(128).map(([b, r]) => b * r).every((v) => v === 128)).toBe(true);
    expect(factorizations(128)).toHaveLength(8);
  });
});
