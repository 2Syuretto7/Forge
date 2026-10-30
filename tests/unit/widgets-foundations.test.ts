import { describe, expect, it } from 'vitest';
import { angleBetween, dot, norms, project } from '../../src/widgets/VectorPlayground';
import { PRESETS as ELIM, eliminate } from '../../src/widgets/EliminationStepper';
import { lstsqLine, makePoints, residualStats } from '../../src/widgets/ProjectionExplorer';
import { PRESETS as EIG, eig2, powerIterate } from '../../src/widgets/EigenFlow';
import { makeMatrix, singularValues, symEigvals, tailError } from '../../src/widgets/SpectrumBars';
import { svd2 } from '../../src/widgets/MatrixTransform';
import { FUNCS as ZOOM, secantSlopes } from '../../src/widgets/TangentZoom';
import { lagrangeBound, taylorCoeffs, taylorEval } from '../../src/widgets/TaylorBuilder';
import { FUNCS as INTEGRANDS, riemann } from '../../src/widgets/RiemannSum';
import { SURFACES, contourSegments, eigSym2, hessian, numGrad } from '../../src/widgets/GradientField';
import { MAPS, jacobian, polygonArea, squareBoundary } from '../../src/widgets/JacobianWarp';

describe('VectorPlayground', () => {
  it('computes the dot product, angle, projection and norms', () => {
    expect(dot([3, 4], [4, -3])).toBe(0);
    expect(angleBetween([1, 1], [1, 0])).toBeCloseTo(Math.PI / 4, 12);
    expect(angleBetween([0.1, 0.2], [0.3, 0.6])).toBeLessThan(1e-15);
    expect(project([3, 4], [2, 0])).toEqual([3, 0]);
    expect(norms([3, -4])).toEqual({ l1: 7, l2: 5, linf: 4 });
  });
});

describe('EliminationStepper', () => {
  it('solves, detects dependent rows and inconsistency', () => {
    const u = eliminate(ELIM.unique.A, ELIM.unique.b, true);
    expect(u.status).toBe('unique');
    u.x!.forEach((v, i) => expect(v).toBeCloseTo([2, 3, -1][i], 12));
    const s = eliminate(ELIM.same.A, ELIM.same.b, true);
    expect(s.status).toBe('infinite');
    expect(s.rank).toBe(2);
    expect(s.residual).toBeLessThan(1e-12);
    expect(eliminate(ELIM.clash.A, ELIM.clash.b, true).status).toBe('none');
  });
  it('needs pivoting for a tiny leading entry', () => {
    const naive = eliminate(ELIM.tiny.A, ELIM.tiny.b, false);
    const piv = eliminate(ELIM.tiny.A, ELIM.tiny.b, true);
    expect(naive.x![0]).toBe(0);
    expect(naive.residual).toBeCloseTo(1, 12);
    expect(piv.x![0]).toBeCloseTo(1, 12);
    expect(piv.residual).toBeLessThan(1e-12);
  });
});

describe('ProjectionExplorer', () => {
  it('leaves a residual perpendicular to both columns at the optimum only', () => {
    for (const outlier of [false, true]) {
      const { xs, ys } = makePoints(14, 7, outlier);
      const { intercept, slope } = lstsqLine(xs, ys);
      const st = residualStats(xs, ys, intercept, slope);
      expect(Math.abs(st.dotOnes)).toBeLessThan(1e-12);
      expect(Math.abs(st.dotX)).toBeLessThan(1e-12);
      expect(residualStats(xs, ys, intercept + 0.1, slope).sse).toBeGreaterThan(st.sse);
      expect(residualStats(xs, ys, intercept, slope - 0.05).sse).toBeGreaterThan(st.sse);
    }
  });
});

describe('EigenFlow', () => {
  it('finds eigenpairs of the presets', () => {
    const s = eig2(...EIG.sym.m);
    expect([s.l1, s.l2]).toEqual([3, 1]);
    expect(Math.abs(s.v1![0] - s.v1![1])).toBeLessThan(1e-12);
    const mk = eig2(...EIG.markov.m);
    expect(mk.l1).toBeCloseTo(1, 12);
    expect(mk.l2).toBeCloseTo(0.4, 12);
    expect(mk.v1![0] / mk.v1![1]).toBeCloseTo(5, 10);
    expect(eig2(...EIG.rotation.m).real).toBe(false);
    expect(eig2(...EIG.shear.m).defective).toBe(true);
  });
  it('converges at the rate |lambda2 / lambda1|', () => {
    const it = powerIterate(EIG.sym.m, [1, 0], 20);
    const tanAngle = (v: [number, number]) => Math.abs((v[0] - v[1]) / (v[0] + v[1]));
    expect(tanAngle(it[11]) / tanAngle(it[10])).toBeCloseTo(1 / 3, 10);
  });
});

describe('SpectrumBars', () => {
  it('Jacobi eigenvalues match known spectra', () => {
    const ev = symEigvals([[2, 1, 0], [1, 2, 0], [0, 0, 5]]);
    expect(ev[0]).toBeCloseTo(5, 12);
    expect(ev[1]).toBeCloseTo(3, 12);
    expect(ev[2]).toBeCloseTo(1, 12);
    const { s1, s2 } = svd2(1.5, 0.5, 0.3, 1);
    const s = singularValues([[1.5, 0.5], [0.3, 1]]);
    expect(s[0]).toBeCloseTo(s1, 10);
    expect(s[1]).toBeCloseTo(s2, 10);
  });
  it('keeps the Frobenius norm and shows the planted rank', () => {
    const A = makeMatrix('planted', 3, 0);
    const s = singularValues(A);
    const fro2 = A.flat().reduce((a, v) => a + v * v, 0);
    expect(s.reduce((a, v) => a + v * v, 0)).toBeCloseTo(fro2, 8);
    expect(s[3] / s[0]).toBeLessThan(1e-6);
    expect(tailError(s, 3).rel).toBeLessThan(1e-6);
    expect(tailError(s, 0).explained).toBe(0);
  });
});

describe('TangentZoom', () => {
  it('secant slopes approach the derivative, but not at a corner', () => {
    const s = secantSlopes(ZOOM.exp.f, 1, 1e-5);
    expect(s.central).toBeCloseTo(Math.E, 8);
    const k = secantSlopes(ZOOM.abs.f, 0, 1e-8);
    expect([k.left, k.right]).toEqual([-1, 1]);
    expect(Number.isNaN(ZOOM.relu.df(0))).toBe(true);
  });
});

describe('TaylorBuilder', () => {
  it('polynomials agree with the functions and respect the remainder bound', () => {
    const c = taylorCoeffs('sin', 0, 9);
    expect(taylorEval(c, 0, 0.1)).toBeCloseTo(Math.sin(0.1), 15);
    for (const n of [2, 5, 8]) {
      const err = Math.abs(taylorEval(taylorCoeffs('exp', 0.5, n), 0.5, 2) - Math.exp(2));
      expect(err).toBeLessThanOrEqual(lagrangeBound('exp', 0.5, 2, n));
    }
    const l = taylorCoeffs('log1p', 0, 40);
    expect(taylorEval(l, 0, 0.5)).toBeCloseTo(Math.log1p(0.5), 10);
    const outside = (n: number) => Math.abs(taylorEval(taylorCoeffs('geom', 0, n), 0, 1.5) - 1 / (1 - 1.5));
    expect(outside(12)).toBeGreaterThan(outside(6));
  });
});

describe('RiemannSum', () => {
  it('has the orders of the classical rules', () => {
    const ratio = (name: string, rule: 'left' | 'mid' | 'trap' | 'simpson') => {
      const { f, a, b, exact } = INTEGRANDS[name];
      return Math.abs(riemann(f, a, b, 16, rule) - exact) / Math.abs(riemann(f, a, b, 32, rule) - exact);
    };
    expect(ratio('square', 'left')).toBeCloseTo(2, 0);
    expect(ratio('sin', 'mid')).toBeCloseTo(4, 1);
    expect(ratio('sin', 'trap')).toBeCloseTo(4, 1);
    expect(ratio('sin', 'simpson')).toBeCloseTo(16, 0);
    for (const F of Object.values(INTEGRANDS)) expect(riemann(F.f, F.a, F.b, 4000, 'mid')).toBeCloseTo(F.exact, 1);
    expect(riemann(INTEGRANDS.beta.f, 0.2, 0.3, 2, 'simpson')).toBeCloseTo(0.112, 14);
    expect(riemann(INTEGRANDS.rsqrt.f, 0, 1, 8, 'left')).toBe(Infinity);
  });
});

describe('GradientField', () => {
  it('gradients, Hessians and contours', () => {
    const g = numGrad(SURFACES.banana.f, [0.5, 0.2]);
    expect(g[0]).toBeCloseTo(-2 * 0.5 - 20 * 0.5 * (0.2 - 0.25), 6);
    expect(g[1]).toBeCloseTo(10 * (0.2 - 0.25), 6);
    const [a, b, d] = hessian(SURFACES.hidden.f, [0, 0]);
    const [l1, l2] = eigSym2(a, b, d);
    expect(l1).toBeCloseTo(5, 3);
    expect(l2).toBeCloseTo(-1, 3);
    const segs = contourSegments(SURFACES.bowl.f, 2, 40, 1);
    expect(segs.length).toBeGreaterThan(20);
    for (const [p] of segs) expect(Math.hypot(...p)).toBeCloseTo(1, 2);
  });
});

describe('JacobianWarp', () => {
  it('area scales by |det J|', () => {
    const J = jacobian(MAPS.polar.f, [0.5, 0.3]);
    expect(J[0] * J[3] - J[1] * J[2]).toBeCloseTo(2 * Math.PI * 0.5, 6);
    const Jd = jacobian(MAPS.disc.f, [0.4, 0.7]);
    expect(Jd[0] * Jd[3] - Jd[1] * Jd[2]).toBeCloseTo(Math.PI, 6);
    const sq = squareBoundary([0.5, 0.3], 0.01, 32);
    expect(polygonArea(sq)).toBeCloseTo(1e-4, 15);
    expect(polygonArea(sq.map(MAPS.polar.f)) / 1e-4).toBeCloseTo(2 * Math.PI * 0.505, 3);
  });
});
