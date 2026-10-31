import { describe, expect, it } from 'vitest';
import { measuredRate, predictedRate, runMethod } from '../../src/widgets/ConvergenceRates';

describe('ConvergenceRates', () => {
  it('measured late rates match the proved rates', () => {
    for (const kappa of [10, 100, 1000]) {
      for (const m of ['gd', 'heavy', 'nesterov'] as const) {
        const e = runMethod(m, kappa, 400);
        const r = measuredRate(e);
        if (e[e.length - 1] > 1e-250) expect(Math.abs(r / predictedRate(m, kappa) - 1)).toBeLessThan(0.01);
      }
    }
  });
  it('momentum beats gradient descent by about the square root of kappa', () => {
    const gd = 1 / -Math.log(predictedRate('gd', 400));
    const hb = 1 / -Math.log(predictedRate('heavy', 400));
    expect(gd / hb).toBeGreaterThan(15);
    expect(gd / hb).toBeLessThan(25);
  });
});
