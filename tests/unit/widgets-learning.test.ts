import { describe, expect, it } from 'vitest';
import { measuredRate, predictedRate, runMethod } from '../../src/widgets/ConvergenceRates';
import { binomTail, chebyshev, hoeffding, hoeffdingEps, normalApprox } from '../../src/widgets/ConcentrationMeter';
import { autocorr, ess, logTarget, metropolis } from '../../src/widgets/MarkovChainSim';
import { A as KKT_A, gradF, kktResidual, solveDisc, solveHalfPlane } from '../../src/widgets/KKTGeometry';

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

describe('KKTGeometry', () => {
  it('half-plane: KKT holds, and an inactive constraint has a zero multiplier', () => {
    const a: [number, number] = [0.8, 0.6];
    const out = solveHalfPlane([1.6, 1.2], a, 1);
    expect(out.active).toBe(true);
    expect(out.lambda).toBeGreaterThan(0);
    const g = a[0] * out.x[0] + a[1] * out.x[1] - 1;
    expect(kktResidual([1.6, 1.2], out.x, out.lambda, g, a)).toBeLessThan(1e-12);
    const free = solveHalfPlane([-1, 0], a, 1);
    expect(free.active).toBe(false);
    expect(free.lambda).toBe(0);
  });
  it('disc: the solution lies on the circle and satisfies stationarity', () => {
    const out = solveDisc([2, -1.5], 1);
    expect(Math.hypot(...out.x)).toBeCloseTo(1, 9);
    const gf = gradF([2, -1.5], out.x);
    expect(Math.abs(gf[0] + 2 * out.lambda * out.x[0])).toBeLessThan(1e-9);
    expect(Math.abs(gf[1] + 2 * out.lambda * out.x[1])).toBeLessThan(1e-9);
    expect(KKT_A[0]).toBe(2);
  });
});

describe('ConcentrationMeter', () => {
  it('the exact tail sits below both bounds, near the normal approximation for large n', () => {
    for (const [n, p, eps] of [[100, 0.5, 0.1], [1000, 0.9, 0.03], [2000, 0.3, 0.02]] as const) {
      const exact = binomTail(n, p, eps);
      expect(exact).toBeLessThanOrEqual(hoeffding(n, eps) + 1e-12);
      expect(exact).toBeLessThanOrEqual(chebyshev(n, p, eps) + 1e-12);
    }
    expect(Math.abs(binomTail(2000, 0.5, 0.02) / normalApprox(2000, 0.5, 0.02) - 1)).toBeLessThan(0.15);
    expect(binomTail(10, 0.5, 0)).toBeCloseTo(1, 12);
    expect(hoeffdingEps(1000, 0.05)).toBeCloseTo(Math.sqrt(Math.log(40) / 2000), 12);
  });
});

describe('MarkovChainSim', () => {
  it('Metropolis samples the target; acceptance falls as the step grows', () => {
    const run = metropolis((x) => logTarget(x, 0), 0, 2.4, 40000);
    const m = run.xs.reduce((a, b) => a + b, 0) / run.xs.length;
    const v = run.xs.reduce((a, b) => a + (b - m) ** 2, 0) / run.xs.length;
    expect(Math.abs(m)).toBeLessThan(0.08);
    expect(Math.abs(v - 1)).toBeLessThan(0.08);
    const rates = [0.1, 1, 10].map((s) => metropolis((x) => logTarget(x, 0), 0, s, 20000).acceptance);
    expect(rates[0]).toBeGreaterThan(rates[1]);
    expect(rates[1]).toBeGreaterThan(rates[2]);
    expect(rates[0]).toBeGreaterThan(0.9);
    expect(rates[2]).toBeLessThan(0.15);
    // The two-peaked target is a half-half mixture of N(-sep/2, 1) and N(sep/2, 1).
    expect(logTarget(2, 4)).toBeCloseTo(Math.log(0.5 + 0.5 * Math.exp(-8)), 12);
  });
  it('autocorrelation and effective sample size of an AR(1) chain match theory', () => {
    let s = 7;
    const r = () => {
      s = (s * 16807) % 2147483647;
      return s / 2147483647;
    };
    const g = () => Math.sqrt(-2 * Math.log(r())) * Math.cos(2 * Math.PI * r());
    const phi = 0.8;
    const xs: number[] = [0];
    for (let i = 1; i < 100000; i++) xs.push(phi * xs[i - 1] + Math.sqrt(1 - phi * phi) * g());
    expect(Math.abs(autocorr(xs, 1) - phi)).toBeLessThan(0.02);
    expect(Math.abs(autocorr(xs, 3) - phi ** 3)).toBeLessThan(0.03);
    const theory = (xs.length * (1 - phi)) / (1 + phi);
    expect(Math.abs(ess(xs) / theory - 1)).toBeLessThan(0.15);
  });
});
