import { describe, expect, it } from 'vitest';
import { svd2 } from '../../src/widgets/MatrixTransform';
import { curve } from '../../src/widgets/BiasVarianceCurve';
import { simulate } from '../../src/widgets/ActivationStats';
import { run, surfaceFns } from '../../src/widgets/LossLandscape';
import { entropy, crossEntropy } from '../../src/widgets/EntropyBars';
import { makeData, stepGD } from '../../src/widgets/DecisionBoundary';
import { ridge, solve } from '../../src/widgets/linalg';

describe('widget numerics', () => {
  it('svd2 reconstructs the matrix', () => {
    const [a, b, c, d] = [1.4, 0.6, 0.2, 0.9];
    const { s1, s2, u1, u2, v1, v2 } = svd2(a, b, c, d);
    const rec = (i: number, j: number) => s1 * [u1[0], u1[1]][i] * [v1[0], v1[1]][j] + s2 * [u2[0], u2[1]][i] * [v2[0], v2[1]][j];
    expect(rec(0, 0)).toBeCloseTo(a, 10);
    expect(rec(0, 1)).toBeCloseTo(b, 10);
    expect(rec(1, 0)).toBeCloseTo(c, 10);
    expect(rec(1, 1)).toBeCloseTo(d, 10);
    expect(s1 * s2).toBeCloseTo(Math.abs(a * d - b * c), 10);
  });

  it('linear solvers are correct', () => {
    expect(solve([[2, 1], [1, 3]], [3, 5])).toEqual([expect.closeTo(0.8, 10), expect.closeTo(1.4, 10)]);
    const Phi = [[1, 0, 1], [0, 1, 1]];
    const w = ridge(Phi, [1, 2], 1e-10); // min-norm interpolant when p > n
    expect(w[0] + w[2]).toBeCloseTo(1, 6);
    expect(w[1] + w[2]).toBeCloseTo(2, 6);
  });

  it('random-feature regression shows double descent near p = n', () => {
    const { test, train } = curve(20, 0.3, -9, 8);
    const at = (p: number) => test[p - 1][1];
    const underBest = Math.min(...test.slice(0, 15).map((t) => t[1]));
    const overBest = Math.min(...test.slice(30).map((t) => t[1]));
    expect(at(20)).toBeGreaterThan(10 * underBest);
    expect(overBest).toBeLessThan(underBest);
    expect(train[39][1]).toBeLessThanOrEqual(1e-6); // interpolation past the threshold (clamped at 1e-6)
    const ridged = curve(20, 0.3, 0, 8).test;
    expect(ridged[19][1]).toBeLessThan(at(20) / 10);
  });

  it('activation statistics follow initialization theory', () => {
    expect(simulate(20, 128, 'small', 'tanh', false, false).actStd[20]).toBeLessThan(1e-10);
    const xav = simulate(20, 128, 'xavier', 'tanh', false, false).actStd[20];
    expect(xav).toBeGreaterThan(0.05);
    expect(xav).toBeLessThan(1);
    const he = simulate(20, 128, 'he', 'relu', false, false).actStd[20];
    expect(he).toBeGreaterThan(0.3);
    expect(he).toBeLessThan(3);
    expect(simulate(20, 128, 'xavier', 'relu', false, false).actStd[20]).toBeLessThan(0.01);
    const unit = simulate(20, 128, 'unit', 'tanh', false, false);
    expect(unit.actStd[20]).toBeGreaterThan(0.8); // saturated: values pinned near +-1
    const res = simulate(30, 128, 'he', 'relu', true, true);
    expect(res.gradStd[0]).toBeGreaterThan(0.5);
    expect(res.gradStd[0]).toBeLessThan(1e3);
  });

  it('gradient descent on a quadratic diverges above lr = 2 / L', () => {
    const { f, g, start } = surfaceFns('quadratic', 10);
    const ok = run('sgd', g, f, start, 0.19, 0, 0, 150, true);
    const bad = run('sgd', g, f, start, 0.21, 0, 0, 150, true);
    expect(ok.losses[ok.losses.length - 1][1]).toBeLessThan(1e-3);
    expect(bad.losses[bad.losses.length - 1][1]).toBeGreaterThan(f(start));
  });

  it('KL divergence is nonnegative and asymmetric', () => {
    const p = [0.7, 0.2, 0.1];
    const q = [0.3, 0.3, 0.4];
    const kl = (a: number[], b: number[]) => crossEntropy(a, b) - entropy(a);
    expect(kl(p, q)).toBeGreaterThan(0);
    expect(kl(p, p)).toBeCloseTo(0, 12);
    expect(Math.abs(kl(p, q) - kl(q, p))).toBeGreaterThan(1e-3);
    expect(entropy([0.5, 0.5], 2)).toBeCloseTo(1, 12);
  });

  it('logistic regression on separable data grows the weight norm', () => {
    const pts = makeData(true, 7);
    let w = [0, 0, 0];
    const norms: number[] = [];
    for (let i = 0; i < 3000; i++) {
      w = stepGD(w, pts, 1, 0).w;
      if (i % 1000 === 999) norms.push(Math.hypot(w[0], w[1]));
    }
    expect(norms[2]).toBeGreaterThan(norms[0] * 1.1);
  });
});
