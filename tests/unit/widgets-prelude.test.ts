import { describe, expect, it } from 'vitest';
import { PRESETS, combine } from '../../src/widgets/MagnitudeLadder';
import { side, solveLinear } from '../../src/widgets/BalanceScale';
import { PAIRS, equivalent, rows } from '../../src/widgets/TruthTable';
import { TARGETS, maxError, reluInterp } from '../../src/widgets/FunctionMachine';
import { partialSums } from '../../src/widgets/SeriesStacker';
import { fitLine } from '../../src/widgets/LogScaler';
import { cis, mul, polar } from '../../src/widgets/UnitCircle';
import { comb, pNoMatch, perm } from '../../src/widgets/CountingTree';

describe('MagnitudeLadder', () => {
  it('adds log centres, and adds half-widths linearly (worst case) or in quadrature (typical)', () => {
    const c = combine([
      { name: 'a', lo: 2, hi: 4 },
      { name: 'b', lo: 1, hi: 3 },
      { name: 'c', lo: 1, hi: 1, divide: true },
    ]);
    expect(c.mid).toBeCloseTo(3 + 2 - 1, 12);
    expect(c.worst).toBeCloseTo(2, 12);
    expect(c.typical).toBeCloseTo(Math.SQRT2, 12);
  });
  it('the presets bracket their computed values', () => {
    for (const p of Object.values(PRESETS)) {
      const c = combine(p.factors);
      expect(Math.abs(c.mid - Math.log10(p.truth))).toBeLessThan(c.worst + 1e-9);
    }
    expect(PRESETS.train.truth).toBeCloseTo(3.333, 3);
  });
});

describe('BalanceScale', () => {
  it('solves a x + b = c x + d in all three cases', () => {
    expect(solveLinear(3, 2, 1, 8)).toEqual({ kind: 'one', x: 3 });
    expect(solveLinear(2, 1, 2, 1)).toEqual({ kind: 'all' });
    expect(solveLinear(2, 1, 2, 5)).toEqual({ kind: 'none' });
    expect(side(3, -2)).toBe('3x - 2');
    expect(side(-1, 0)).toBe('-x');
  });
});

describe('TruthTable', () => {
  it('knows which pairs are equivalent', () => {
    expect(equivalent(PAIRS.contrapositive)).toBe(true);
    expect(equivalent(PAIRS.orform)).toBe(true);
    expect(equivalent(PAIRS.demorgan)).toBe(true);
    expect(equivalent(PAIRS.distribute)).toBe(true);
    expect(equivalent(PAIRS.converse)).toBe(false);
    expect(equivalent(PAIRS.wrongDemorgan)).toBe(false);
    expect(rows(PAIRS.distribute)).toHaveLength(8);
    expect(rows(PAIRS.converse).filter((r) => r.a !== r.b)).toHaveLength(2);
  });
});

describe('FunctionMachine', () => {
  it('interpolates exactly at the knots and needs about 30 pieces for a hill to 0.01', () => {
    const f = TARGETS.bump[1];
    const fit = reluInterp(f, 7, -3, 3);
    for (const t of fit.knots) expect(fit.evaluate(t)).toBeCloseTo(f(t), 12);
    const err = (n: number) => maxError(f, reluInterp(f, n, -3, 3).evaluate, -3, 3);
    expect(err(29)).toBeGreaterThan(0.01);
    expect(err(31)).toBeLessThan(0.01);
    expect(err(20) / err(40)).toBeGreaterThan(3.5);
  });
});

describe('SeriesStacker', () => {
  it('partial sums approach their limits', () => {
    expect(partialSums('geometric', 60, 0.5)[59]).toBeCloseTo(2, 12);
    expect(partialSums('squares', 10000)[9999]).toBeCloseTo(Math.PI ** 2 / 6, 3);
    expect(partialSums('alternating', 100000)[99999]).toBeCloseTo(Math.LN2, 4);
    const h = partialSums('harmonic', 1e6);
    expect(h[999999] - Math.log(1e6)).toBeCloseTo(0.5772156649, 5);
  });
});

describe('LogScaler', () => {
  it('fits a line and reports the exponent of a power law in log-log axes', () => {
    const xs = [1, 2, 4, 8, 16];
    const f = fitLine(
      xs.map(Math.log10),
      xs.map((x) => Math.log10(3 * x ** 2.5)),
    );
    expect(f.slope).toBeCloseTo(2.5, 12);
    expect(f.r2).toBeCloseTo(1, 12);
  });
});

describe('UnitCircle', () => {
  it('multiplying complex numbers multiplies lengths and adds angles', () => {
    const z = mul(cis(0.5, 2), cis(0.7, 1.5));
    expect(polar(z).r).toBeCloseTo(3, 12);
    expect(polar(z).theta).toBeCloseTo(1.2, 12);
    expect(mul([0, 1], [0, 1])).toEqual([-1, 0]);
  });
});

describe('CountingTree', () => {
  it('counts arrangements, selections and birthday collisions', () => {
    expect(perm(5, 3)).toBe(60);
    expect(comb(5, 3)).toBe(10);
    expect(comb(52, 5)).toBe(2598960);
    expect(1 - pNoMatch(23)).toBeCloseTo(0.5073, 4);
    expect(1 - pNoMatch(22)).toBeLessThan(0.5);
  });
});
