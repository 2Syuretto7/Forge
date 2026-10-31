import { describe, expect, it } from 'vitest';
import { bbpOutlier, mpDensity, mpEdges, sampleCovEigs } from '../../src/widgets/RandomSpectrum';
import { sampleVariance, theoryVariance } from '../../src/widgets/EstimatorVariance';
import { density, reverseRun, score, w1ToMixture } from '../../src/widgets/DiffusionStepper';

describe('RandomSpectrum', () => {
  it('the Marchenko-Pastur density integrates to 1 between its edges', () => {
    for (const g of [0.1, 0.25, 0.5, 0.9]) {
      const [a, b] = mpEdges(g);
      const N = 200000;
      let s = 0;
      for (let i = 0; i < N; i++) s += mpDensity(a + ((b - a) * (i + 0.5)) / N, g) * ((b - a) / N);
      expect(Math.abs(s - 1)).toBeLessThan(2e-3);
    }
  });
  it('sample eigenvalues fill the predicted bulk and a strong spike escapes it', () => {
    const e = sampleCovEigs(100, 0.25);
    const [a, b] = mpEdges(0.25);
    expect(Math.abs(e[0] - b)).toBeLessThan(0.25);
    expect(Math.abs(e[e.length - 1] - a)).toBeLessThan(0.1);
    expect(Math.abs(e.reduce((s, v) => s + v, 0) / e.length - 1)).toBeLessThan(0.05);
    // The top eigenvalue fluctuates by several percent at this size; average a few draws.
    const top = [1, 2, 3, 4].map((seed) => sampleCovEigs(100, 0.25, 3, seed)[0]).reduce((s, v) => s + v, 0) / 4;
    expect(Math.abs(top / bbpOutlier(3, 0.25) - 1)).toBeLessThan(0.08);
    expect(bbpOutlier(0.3, 0.25)).toBe(b);
  });
});

describe('EstimatorVariance', () => {
  it('measured variances match (d + 2)(d + 4), 2d + 8 and 4 at mu = 0, and all three are unbiased', () => {
    for (const d of [1, 8, 32]) {
      for (const est of ['score', 'baseline', 'reparam'] as const) {
        const { mean, variance } = sampleVariance(est, d, 0, 40000, 11);
        expect(Math.abs(variance / theoryVariance(est, d) - 1)).toBeLessThan(0.12);
        expect(Math.abs(mean)).toBeLessThan(4 * Math.sqrt(theoryVariance(est, d) / 40000));
      }
    }
    const shifted = sampleVariance('reparam', 4, 1.5, 40000, 12);
    expect(Math.abs(shifted.mean - 3)).toBeLessThan(0.05);
  });
});

describe('DiffusionStepper', () => {
  it('the score is the derivative of the log density, and the reverse run recovers the data', () => {
    for (const t of [0.01, 0.5, 2]) {
      for (const x of [-2.5, 0, 1.2]) {
        const h = 1e-5;
        const num = (Math.log(density(x + h, t)) - Math.log(density(x - h, t))) / (2 * h);
        expect(Math.abs(num - score(x, t))).toBeLessThan(1e-5);
      }
    }
    const fine = reverseRun(3000, 100, 4, 5);
    const coarse = reverseRun(3000, 5, 4, 5);
    const end = (s: { t: number; x: number[] }[]) => s[s.length - 1];
    expect(w1ToMixture(end(fine).x, end(fine).t)).toBeLessThan(0.08);
    expect(w1ToMixture(end(coarse).x, end(coarse).t)).toBeGreaterThan(2 * w1ToMixture(end(fine).x, end(fine).t));
    expect(w1ToMixture(fine[0].x, 4)).toBeLessThan(0.08);
  });
});
