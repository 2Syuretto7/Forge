import { describe, expect, it } from 'vitest';
import { addDays, grade, newReview } from '../../src/review/sm2';

describe('SM-2 scheduler', () => {
  it('schedules a new item for the next day', () => {
    expect(newReview('a', '2026-03-01').due).toBe('2026-03-02');
  });
  it('follows 1, 6, then interval * ease for good grades', () => {
    let r = newReview('a', '2026-03-01');
    r = grade(r, 5, '2026-03-02');
    expect(r.interval).toBe(1);
    r = grade(r, 5, '2026-03-03');
    expect(r.interval).toBe(6);
    const ease = r.ease;
    r = grade(r, 5, '2026-03-09');
    expect(r.interval).toBe(Math.round(6 * ease));
    expect(r.reps).toBe(3);
  });
  it('resets on a failing grade and lowers ease, never below 1.3', () => {
    let r = newReview('a', '2026-03-01');
    for (let i = 0; i < 10; i++) r = grade(r, 0, '2026-03-02');
    expect(r.reps).toBe(0);
    expect(r.interval).toBe(1);
    expect(r.lapses).toBe(10);
    expect(r.ease).toBeCloseTo(1.3);
  });
  it('adds days across month boundaries', () => {
    expect(addDays('2026-01-30', 3)).toBe('2026-02-02');
  });
});
