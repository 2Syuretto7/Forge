import { describe, expect, it } from 'vitest';
import { bbpOutlier, mpDensity, mpEdges, sampleCovEigs } from '../../src/widgets/RandomSpectrum';

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
